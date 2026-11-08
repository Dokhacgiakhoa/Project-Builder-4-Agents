"""Data models for Auditor Engine criteria and findings."""


class CriterionItem(dict):
    """Mỗi tiêu chuẩn kiểm tra có chứng cứ thực tế từ mã nguồn (file, dòng, snippet, chi tiết cụ thể).

    Thừa kế dict để tương thích hoàn toàn với json.dumps() và API serialization.
    Đồng thời hỗ trợ kiểm tra chuỗi (substring check qua __contains__) và str() để
    hoàn toàn tương thích ngược với logic cũ.
    """

    def __init__(
        self,
        title: str,
        evidence: str = "",
        snippet: str = "",
        details: str = "",
        badge: str = "",
        remediation: str = "",
        location: str = "",
        severity: str = "Trung bình",
    ):
        super().__init__(
            title=title,
            evidence=str(evidence or ""),
            snippet=str(snippet or ""),
            details=str(details or ""),
            badge=str(badge or ""),
            remediation=str(remediation or ""),
            location=str(location or ""),
            severity=str(severity or "Trung bình"),
        )

    def __contains__(self, item):
        # Hỗ trợ cả tra cứu key ('title' in item) và tra cứu chuỗi con ('DESIGN TOKENS' in item)
        if super().__contains__(item):
            return True
        if isinstance(item, str):
            t = self.get("title", "")
            d = self.get("details", "")
            s = self.get("snippet", "")
            return item in t or item in d or item in s
        return False

    def __str__(self):
        return self.get("title", "")

    @property
    def title(self):
        return self.get("title", "")

    @property
    def evidence(self):
        return self.get("evidence", "")

    @property
    def snippet(self):
        return self.get("snippet", "")

    @property
    def details(self):
        return self.get("details", "")

    @property
    def badge(self):
        return self.get("badge", "")

    @property
    def remediation(self):
        return self.get("remediation", "")

    @property
    def severity(self):
        return self.get("severity", "Trung bình")

    @property
    def is_critical(self):
        return self.get("severity") == "Cao"
