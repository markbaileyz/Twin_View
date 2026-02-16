from app.correlator.normalizer import compute_signature, normalize


def test_normalize_redacts_patterns():
    msg = "VM 12345 at 2024-01-01T12:00:00Z from 10.1.2.3 uuid 123e4567-e89b-12d3-a456-426614174000 hex abcdef1234"
    out = normalize(msg)
    assert "<NUM>" in out
    assert "<TS>" in out
    assert "<IP>" in out
    assert "<UUID>" in out
    assert "<HEX>" in out


def test_compute_signature_stable():
    a = compute_signature("alarm", normalize("Host abc"), "h1", "demo")
    b = compute_signature("alarm", normalize("Host abc"), "h1", "demo")
    assert a == b
    assert len(a) == 16
