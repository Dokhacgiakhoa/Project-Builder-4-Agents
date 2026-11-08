"""Nhận định: đối chiếu Project Model với Knowledge Pack, sinh điểm mạnh / điểm nghẽn / đề xuất kèm bằng chứng.

Logic thuần, sinh theo mẫu (không gọi model). Mỗi nhận định trỏ tới dữ liệu đo và mã tài liệu kit liên quan.
"""

from __future__ import annotations

from .knowledge import doc_by_id, profile_docs

SLUG_LABEL = {
    'simple-layered': 'Phân tầng đơn giản', 'clean-architecture': 'Clean Architecture',
    'vertical-slice': 'Vertical Slice', 'modular-monolith': 'Modular Monolith',
}
SEVERITY_ORDER = {'Cao': 0, 'Trung bình': 1, 'Thấp': 2}
# điểm nghẽn -> tài liệu kit nên đọc
DOCS_FOR = {
    'cycle': ['S-004', 'K-004'], 'layer': ['K-004'], 'tests': ['S-002', 'S-003'], 'large': ['S-001', 'S-004'],
    'manifest': ['K-003'], 'profile': ['K-004'],
}
ACTION = {
    'cycle': 'Phá vòng phụ thuộc: tách phần dùng chung ra thành phần riêng hoặc đảo hướng phụ thuộc qua interface.',
    'layer': 'Sửa import ngược hướng: tầng trong chỉ phụ thuộc tầng trong/hợp đồng, đưa chi tiết hạ tầng ra ngoài.',
    'tests': 'Bổ sung test hồi quy cho luồng chính trước khi tiếp tục thêm tính năng.',
    'large': 'Tách các tệp quá lớn theo trách nhiệm; mỗi tệp một lý do thay đổi.',
    'manifest': 'Khai báo đầy đủ phụ thuộc (lockfile/requirements) để dựng lại môi trường và quét chuỗi cung ứng.',
    'profile': 'Chọn lại profile kiến trúc cho khớp thực tế hoặc chỉnh cấu trúc cho khớp profile đã khai báo.',
}
FORBIDDEN_FLOW = {('domain', 'infrastructure'), ('domain', 'presentation'), ('domain', 'application'),
                  ('application', 'presentation'), ('infrastructure', 'presentation'), ('infrastructure', 'application')}


def _layer_violations(model: dict) -> list[str]:
    layer = {c['name']: c['layer'] for c in model['components'] if c.get('layer') and c['role'] == 'code'}
    out = []
    for e in model['edges']:
        a, b = layer.get(e['from']), layer.get(e['to'])
        if a and b and (a, b) in FORBIDDEN_FLOW:
            out.append(f"{e['from']} ({a}) → {e['to']} ({b}), {e['count']} import")
    return out


def recommend_profile(model: dict, pack: dict) -> dict:
    """Chọn profile kiến trúc phù hợp nhất theo cấu trúc, quy mô, và `when` / `not_when` của kit."""
    profiles = profile_docs(pack)
    code_comps = [c for c in model['components'] if c['role'] == 'code']
    loc = model['code_loc'] - model['test_loc']
    style = model['architecture']['style']
    reasons = []
    if loc < 1:
        return {'slug': None, 'reasons': ['Không có mã nguồn đáng kể: profile kiến trúc chưa áp dụng.']}
    if style in SLUG_LABEL:
        slug = style
        reasons.append(f"Cấu trúc và hướng import hiện tại khớp mẫu {SLUG_LABEL[slug]}.")
    elif loc < 6000 or len(code_comps) < 4:
        slug = 'simple-layered'
        reasons.append(f'Quy mô {loc} dòng mã / {len(code_comps)} thành phần: đủ nhỏ cho mẫu phân tầng đơn giản.')
    else:
        slug = 'modular-monolith'
        reasons.append(f'{len(code_comps)} thành phần, {loc} dòng mã: nên có ranh giới module rõ ràng.')
    doc = profiles.get(slug)
    if not doc:
        return {'slug': slug, 'reasons': reasons}
    if slug == 'clean-architecture' and loc < 3000:
        reasons.append(f"Lưu ý `not_when` của kit: \"{doc.get('not_when', '')}\" — dự án còn nhỏ, cân nhắc chi phí tầng.")
    return {'slug': slug, 'doc_id': doc['id'], 'title': doc.get('title', ''), 'when': doc.get('when', ''),
            'not_when': doc.get('not_when', ''), 'path': doc.get('path', ''), 'reasons': reasons}


def _checklist(profile: dict, pack: dict, model: dict, violations: list[str]) -> list[dict]:
    doc = doc_by_id(pack, profile.get('doc_id', '')) if profile.get('doc_id') else None
    if not doc:
        return []
    big = model['hotspots']['large_files']
    items = []
    for section, label in (('constraints', 'Constraints'), ('common_mistakes', 'Common mistakes')):
        for text in (doc.get('sections', {}).get(section) or [])[:6]:
            low = text.lower()
            status, evidence = 'unverified', 'Cần người/agent xác nhận (không đo được bằng phân tích tĩnh).'
            if '→' in text and 'dependency' in low:
                status = 'violated' if violations else 'ok'
                evidence = '; '.join(violations[:3]) if violations else 'Không thấy import ngược chiều giữa các tầng đã nhận diện.'
            elif 'god' in low or '350' in low:
                status = 'violated' if big else 'ok'
                evidence = ', '.join(f"{b['file']} ({b['loc']} dòng)" for b in big[:3]) if big else 'Không có tệp ≥ 350 dòng.'
            elif 'test' in low:
                ok = model['test_ratio'] >= 0.1
                status = 'ok' if ok else 'violated'
                evidence = f"Tỷ lệ dòng test / dòng mã: {model['test_ratio']}."
            items.append({'source': f"{doc['id']} · {label}", 'text': text, 'status': status, 'evidence': evidence})
    return items


def build_insights(model: dict, pack: dict, declared_arch: str | None = None) -> dict:
    bottlenecks, strengths = [], []
    code_loc, test_ratio = model['code_loc'] - model['test_loc'], model['test_ratio']
    violations = _layer_violations(model) or model['architecture']['violations']

    if model['cycles']:
        bottlenecks.append({
            'severity': 'Trung bình', 'key': 'cycle',
            'title': f"Phụ thuộc vòng giữa {len(model['cycles'])} nhóm thành phần",
            'evidence': ['; '.join(' ↔ '.join(g) for g in model['cycles'][:3])],
            'why': 'Vòng phụ thuộc khiến sửa một nơi kéo theo nhiều nơi khác và cản trở tách module / test độc lập.'})
    elif len(model['components']) >= 3:
        strengths.append({'text': 'Không có phụ thuộc vòng giữa các thành phần.',
                          'evidence': [f"{len(model['components'])} thành phần, {len(model['edges'])} cạnh phụ thuộc."]})
    if violations:
        bottlenecks.append({
            'severity': 'Cao', 'key': 'layer', 'title': 'Import ngược hướng giữa các tầng kiến trúc',
            'evidence': violations[:4],
            'why': 'Tầng trong (domain/service) không nên biết tầng ngoài (UI/hạ tầng); vi phạm làm khó thay thế và kiểm thử.'})
    if code_loc >= 300:
        if model['test_loc'] == 0:
            bottlenecks.append({'severity': 'Cao', 'key': 'tests', 'title': 'Chưa phát hiện test nào',
                                'evidence': [f'{code_loc} dòng mã, 0 dòng test.'],
                                'why': 'Agent và người sửa code không có lưới an toàn để biết thay đổi có làm hỏng gì không.'})
        elif test_ratio < 0.1:
            bottlenecks.append({'severity': 'Trung bình', 'key': 'tests', 'title': 'Độ phủ test mỏng so với quy mô mã',
                                'evidence': [f"{model['test_loc']} dòng test / {code_loc} dòng mã (tỷ lệ {test_ratio})."],
                                'why': 'Phần lớn logic chưa có test hồi quy.'})
        elif test_ratio >= 0.3:
            strengths.append({'text': 'Có bộ test tương xứng với quy mô mã.',
                              'evidence': [f"{model['test_loc']} dòng test / {code_loc} dòng mã (tỷ lệ {test_ratio})."]})
    big = model['hotspots']['large_files']
    if big:
        worst = big[0]
        bottlenecks.append({
            'severity': 'Trung bình' if worst['loc'] >= 800 else 'Thấp', 'key': 'large',
            'title': f"{len(big)} tệp quá lớn (≥ 350 dòng)",
            'evidence': [f"{b['file']}: {b['loc']} dòng" for b in big[:4]],
            'why': 'Tệp quá lớn thường gom nhiều trách nhiệm, khó đọc cho cả người lẫn agent và dễ phát sinh vá víu.'})
    if code_loc >= 500 and not model['stack'] and model['languages']:
        bottlenecks.append({'severity': 'Thấp', 'key': 'manifest', 'title': 'Không nhận diện được phụ thuộc khai báo',
                            'evidence': ['Không thấy package.json / requirements / csproj có khai báo thư viện.'],
                            'why': 'Thiếu khai báo phụ thuộc làm khó tái dựng môi trường và quét chuỗi cung ứng.'})
    if model['doc_loc'] >= max(code_loc // 2, 200):
        strengths.append({'text': 'Có lượng tài liệu đáng kể đi kèm mã.',
                          'evidence': [f"{model['doc_loc']} dòng tài liệu so với {code_loc} dòng mã."]})
    if model['entrypoints']:
        strengths.append({'text': 'Điểm vào chương trình rõ ràng.', 'evidence': model['entrypoints'][:3]})

    profile = recommend_profile(model, pack)
    declared_note = None
    if declared_arch in SLUG_LABEL and profile.get('slug') and declared_arch != profile['slug']:
        declared_note = (f"Dự án khai báo profile `{declared_arch}` nhưng phân tích gợi ý `{profile['slug']}`: "
                         "kiểm tra lại khai báo hoặc cấu trúc thực.")
        bottlenecks.append({'severity': 'Thấp', 'key': 'profile', 'title': 'Profile khai báo lệch với cấu trúc thực',
                            'evidence': [declared_note], 'why': 'Rào chắn theo profile chỉ có ý nghĩa khi khớp thực tế.'})

    bottlenecks.sort(key=lambda b: SEVERITY_ORDER[b['severity']])
    recommendations = []
    for b in bottlenecks:
        ids = [i for i in DOCS_FOR.get(b['key'], []) if doc_by_id(pack, i)]
        if profile.get('doc_id') and b['key'] in ('layer', 'cycle', 'profile'):
            ids = [profile['doc_id']] + ids
        recommendations.append({'priority': b['severity'], 'action': ACTION[b['key']], 'reason': b['title'],
                                'doc_ids': ids})

    langs = ', '.join(f"{l['name']} {l['share']}%" for l in model['languages'][:3]) or 'không rõ'
    stack = ', '.join(s['name'] for s in model['stack'][:8]) or 'chưa nhận diện thư viện đáng chú ý'
    kind = model['kind']
    central = model['hotspots']['central_components']
    summary = [
        f"Dự án chủ yếu viết bằng {langs}. Loại hình nhận diện: **{kind['label']}**"
        + (f" ({'; '.join(kind['secondary'])})" if kind['secondary'] else '') + '.',
        f"Quy mô: {code_loc} dòng mã ({model['files_analyzed']} tệp), {model['test_loc']} dòng test, "
        f"{model['doc_loc']} dòng tài liệu.",
        f"Thư viện / framework nhận diện từ import thực: {stack}.",
        f"Cấu trúc: {model['architecture']['label']} (độ tin cậy {model['architecture']['confidence']}), "
        f"{len(model['components'])} thành phần" + (f", trung tâm phụ thuộc: {', '.join(central)}" if central else '') + '.',
    ]
    if profile.get('slug'):
        summary.append(f"Đối chiếu kit: profile phù hợp nhất là **{SLUG_LABEL[profile['slug']]}** ({profile.get('doc_id', '')}).")
    return {
        'summary': summary, 'profile': {**profile, 'declared': declared_arch, 'declared_note': declared_note},
        'strengths': strengths, 'bottlenecks': bottlenecks, 'recommendations': recommendations,
        'checklist': _checklist(profile, pack, model, violations),
        'pack': {'generated': pack.get('generated', ''), 'source': pack.get('source', ''), 'docs': len(pack.get('docs', []))},
        'limits': ['Phân tích tĩnh: không thấy import động/reflection.',
                   f"Độ tin cậy kiến trúc {model['architecture']['confidence']}."
                   + (' Đã cắt bớt vì dự án rất lớn.' if model['truncated'] else '')],
    }
