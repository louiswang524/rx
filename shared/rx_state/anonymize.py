import re

_SELFREF = re.compile(r"our (prior|previous) work", re.IGNORECASE)
_ACK = re.compile(r"acknowledg|funding", re.IGNORECASE)


def anonymize_text(text: str, author_names: list[str], self_urls: list[str]) -> str:
    out = text
    for name in author_names:
        out = re.sub(re.escape(name), "Anonymous", out, flags=re.IGNORECASE)
    for url in self_urls:
        out = re.sub(re.escape(url), "[ANONYMIZED-URL]", out, flags=re.IGNORECASE)
    out = _SELFREF.sub(lambda m: f"{m.group(1)} work", out)
    return out


def lint_anonymity(text: str, author_names: list[str], self_urls: list[str]) -> list[str]:
    findings: list[str] = []
    for name in author_names:
        if re.search(re.escape(name), text, re.IGNORECASE):
            findings.append(f"author name present: {name}")
    for url in self_urls:
        if re.search(re.escape(url), text, re.IGNORECASE):
            findings.append(f"self URL present: {url}")
    if _SELFREF.search(text):
        findings.append('self-identifying phrase: "our prior/previous work"')
    if _ACK.search(text):
        findings.append("acknowledgment/funding mention present")
    return findings
