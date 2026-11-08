"""Nhận định: đối chiếu Project Model với Knowledge Pack, sinh điểm mạnh / điểm nghẽn / đề xuất kèm bằng chứng.

Logic thuần, sinh theo mẫu (không gọi model). Mỗi nhận định trỏ tới dữ liệu đo và mã tài liệu kit liên quan.
"""

from __future__ import annotations

from .knowledge import doc_by_id, profile_docs

SLUG_LABEL = {
    'simple-layered': 'Simple layered', 'clean-architecture': 'Clean Architecture',
    'vertical-slice': 'Vertical Slice', 'modular-monolith': 'Modular Monolith',
}
SEVERITY_ORDER = {'High': 0, 'Medium': 1, 'Low': 2}
# điểm nghẽn -> tài liệu kit nên đọc
DOCS_FOR = {
    'cycle': ['S-004', 'K-004'], 'layer': ['K-004'], 'tests': ['S-002', 'S-003'], 'large': ['S-001', 'S-004'],
    'manifest': ['K-003'], 'profile': ['K-004'],
}
ACTION = {
    'cycle': 'Break the dependency cycle: extract the shared part into its own component or invert the dependency through an interface.',
    'layer': 'Fix backward imports: inner layers may depend only on inner layers/contracts; move infrastructure details outward.',
    'tests': 'Add regression tests for the main flow before adding more features.',
    'large': 'Split oversized files by responsibility; one reason to change per file.',
    'manifest': 'Declare all dependencies completely (lockfile/requirements) so the environment can be rebuilt and the supply chain scanned.',
    'profile': 'Re-pick the architecture profile to match reality, or adjust the structure to match the declared profile.',
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
        return {'slug': None, 'reasons': ['No significant source code: the architecture profile does not apply yet.']}
    if style in SLUG_LABEL:
        slug = style
        reasons.append(f"The current structure and import direction match the {SLUG_LABEL[slug]} pattern.")
    elif loc < 6000 or len(code_comps) < 4:
        slug = 'simple-layered'
        reasons.append(f'Size {loc} lines of code / {len(code_comps)} components: small enough for the simple layered pattern.')
    else:
        slug = 'modular-monolith'
        reasons.append(f'{len(code_comps)} components, {loc} lines of code: clear module boundaries are advisable.')
    doc = profiles.get(slug)
    if not doc:
        return {'slug': slug, 'reasons': reasons}
    if slug == 'clean-architecture' and loc < 3000:
        reasons.append(f"Kit `not_when` note: \"{doc.get('not_when', '')}\" — the project is still small, weigh the cost of layering.")
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
            status, evidence = 'unverified', 'Needs human/agent confirmation (cannot be measured by static analysis).'
            if '→' in text and 'dependency' in low:
                status = 'violated' if violations else 'ok'
                evidence = '; '.join(violations[:3]) if violations else 'No backward imports found between the detected layers.'
            elif 'god' in low or '350' in low:
                status = 'violated' if big else 'ok'
                evidence = ', '.join(f"{b['file']} ({b['loc']} lines)" for b in big[:3]) if big else 'No files of ≥ 350 lines.'
            elif 'test' in low:
                ok = model['test_ratio'] >= 0.1
                status = 'ok' if ok else 'violated'
                evidence = f"Test-to-code line ratio: {model['test_ratio']}."
            items.append({'source': f"{doc['id']} · {label}", 'text': text, 'status': status, 'evidence': evidence})
    return items


def build_insights(model: dict, pack: dict, declared_arch: str | None = None) -> dict:
    bottlenecks, strengths = [], []
    code_loc, test_ratio = model['code_loc'] - model['test_loc'], model['test_ratio']
    violations = _layer_violations(model) or model['architecture']['violations']

    if model['cycles']:
        bottlenecks.append({
            'severity': 'Medium', 'key': 'cycle',
            'title': f"Circular dependencies between {len(model['cycles'])} component groups",
            'evidence': ['; '.join(' ↔ '.join(g) for g in model['cycles'][:3])],
            'why': 'Dependency cycles make a change in one place ripple into many others and block module splitting / independent testing.'})
    elif len(model['components']) >= 3:
        strengths.append({'text': 'No circular dependencies between components.',
                          'evidence': [f"{len(model['components'])} components, {len(model['edges'])} dependency edges."]})
    if violations:
        bottlenecks.append({
            'severity': 'High', 'key': 'layer', 'title': 'Backward imports between architecture layers',
            'evidence': violations[:4],
            'why': 'Inner layers (domain/service) should not know outer layers (UI/infrastructure); violations make replacement and testing harder.'})
    if code_loc >= 300:
        if model['test_loc'] == 0:
            bottlenecks.append({'severity': 'High', 'key': 'tests', 'title': 'No tests detected yet',
                                'evidence': [f'{code_loc} lines of code, 0 test lines.'],
                                'why': 'Agents and people editing the code have no safety net to know whether a change breaks anything.'})
        elif test_ratio < 0.1:
            bottlenecks.append({'severity': 'Medium', 'key': 'tests', 'title': 'Thin test coverage relative to code size',
                                'evidence': [f"{model['test_loc']} test lines / {code_loc} lines of code (ratio {test_ratio})."],
                                'why': 'Most logic has no regression tests yet.'})
        elif test_ratio >= 0.3:
            strengths.append({'text': 'A test suite proportional to the code size exists.',
                              'evidence': [f"{model['test_loc']} test lines / {code_loc} lines of code (ratio {test_ratio})."]})
    big = model['hotspots']['large_files']
    if big:
        worst = big[0]
        bottlenecks.append({
            'severity': 'Medium' if worst['loc'] >= 800 else 'Low', 'key': 'large',
            'title': f"{len(big)} oversized files (≥ 350 lines)",
            'evidence': [f"{b['file']}: {b['loc']} lines" for b in big[:4]],
            'why': 'Oversized files usually bundle many responsibilities, are hard to read for people and agents alike, and invite patchwork.'})
    if code_loc >= 500 and not model['stack'] and model['languages']:
        bottlenecks.append({'severity': 'Low', 'key': 'manifest', 'title': 'Declared dependencies not detected',
                            'evidence': ['No package.json / requirements / csproj declaring libraries found.'],
                            'why': 'Missing dependency declarations make it hard to rebuild the environment and scan the supply chain.'})
    if model['doc_loc'] >= max(code_loc // 2, 200):
        strengths.append({'text': 'A substantial amount of documentation accompanies the code.',
                          'evidence': [f"{model['doc_loc']} documentation lines vs {code_loc} lines of code."]})
    if model['entrypoints']:
        strengths.append({'text': 'Clear program entry points.', 'evidence': model['entrypoints'][:3]})

    profile = recommend_profile(model, pack)
    declared_note = None
    if declared_arch in SLUG_LABEL and profile.get('slug') and declared_arch != profile['slug']:
        declared_note = (f"The project declares profile `{declared_arch}` but the analysis suggests `{profile['slug']}`: " "re-check the declaration or the actual structure.")
        bottlenecks.append({'severity': 'Low', 'key': 'profile', 'title': 'Declared profile differs from the actual structure',
                            'evidence': [declared_note], 'why': 'Profile guardrails only matter when they match reality.'})

    bottlenecks.sort(key=lambda b: SEVERITY_ORDER[b['severity']])
    recommendations = []
    for b in bottlenecks:
        ids = [i for i in DOCS_FOR.get(b['key'], []) if doc_by_id(pack, i)]
        if profile.get('doc_id') and b['key'] in ('layer', 'cycle', 'profile'):
            ids = [profile['doc_id']] + ids
        recommendations.append({'priority': b['severity'], 'action': ACTION[b['key']], 'reason': b['title'],
                                'doc_ids': ids})

    langs = ', '.join(f"{l['name']} {l['share']}%" for l in model['languages'][:3]) or 'unknown'
    stack = ', '.join(s['name'] for s in model['stack'][:8]) or 'no notable libraries detected'
    kind = model['kind']
    central = model['hotspots']['central_components']
    summary = [
        f"The project is mainly written in {langs}. Detected project type: **{kind['label']}**"
        + (f" ({'; '.join(kind['secondary'])})" if kind['secondary'] else '') + '.',
        f"Size: {code_loc} lines of code ({model['files_analyzed']} files), {model['test_loc']} test lines, " f"{model['doc_loc']} documentation lines.",
        f"Libraries / frameworks detected from real imports: {stack}.",
        f"Structure: {model['architecture']['label']} (confidence {model['architecture']['confidence']}), " f"{len(model['components'])} components" + (f", dependency hubs: {', '.join(central)}" if central else '') + '.',
    ]
    if profile.get('slug'):
        summary.append(f"Kit comparison: the best-fitting profile is **{SLUG_LABEL[profile['slug']]}** ({profile.get('doc_id', '')}).")
    return {
        'summary': summary, 'profile': {**profile, 'declared': declared_arch, 'declared_note': declared_note},
        'strengths': strengths, 'bottlenecks': bottlenecks, 'recommendations': recommendations,
        'checklist': _checklist(profile, pack, model, violations),
        'pack': {'generated': pack.get('generated', ''), 'source': pack.get('source', ''), 'docs': len(pack.get('docs', []))},
        'limits': ['Static analysis: no dynamic imports/reflection seen.',
                   f"Architecture confidence {model['architecture']['confidence']}."
                   + (' Truncated because the project is very large.' if model['truncated'] else '')],
    }
