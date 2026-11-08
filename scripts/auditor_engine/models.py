"""Data models for Auditor Engine criteria and findings."""


class CriterionItem(dict):
    """Each check criterion carries real evidence from the source (file, line, snippet, concrete detail).

    Inherits dict for full compatibility with json.dumps() and API serialization.
    Also supports string checks (substring check via __contains__) and str() to be
    fully backward compatible with the old logic.
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
        severity: str = "Medium",
    ):
        super().__init__(
            title=title,
            evidence=str(evidence or ""),
            snippet=str(snippet or ""),
            details=str(details or ""),
            badge=str(badge or ""),
            remediation=str(remediation or ""),
            location=str(location or ""),
            severity=str(severity or "Medium"),
        )

    def __contains__(self, item):
        # Supports both key lookups ('title' in item) and substring lookups ('DESIGN TOKENS' in item)
        if super().__contains__(item):
            return True
        if isinstance(item, str):
            # Case-insensitive on purpose: engine text is English and its casing must not change results.
            needle = item.casefold()
            return any(needle in str(self.get(k, "")).casefold() for k in ("title", "details", "snippet"))
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
        return self.get("severity", "Medium")

    @property
    def is_critical(self):
        return self.get("severity") == "High"
