import hashlib
import re

UUID_RE = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
HEX_RE = re.compile(r"\b[0-9a-f]{8,}\b", re.I)
NUM_RE = re.compile(r"\b\d{4,}\b")
TS_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?\b")
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def normalize(message: str) -> str:
    text = (message or "").lower()
    text = UUID_RE.sub("<UUID>", text)
    text = HEX_RE.sub("<HEX>", text)
    text = NUM_RE.sub("<NUM>", text)
    text = TS_RE.sub("<TS>", text)
    text = IP_RE.sub("<IP>", text)
    return " ".join(text.split())


def compute_signature(category: str, normalized_message: str, entity: str | None, source_type: str) -> str:
    raw = f"{category}|{normalized_message}|{entity or ''}|{source_type}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]
