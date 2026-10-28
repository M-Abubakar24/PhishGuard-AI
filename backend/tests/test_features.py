
import pytest

from backend.app.features import extract_url_features


def test_extracts_https_feature():
    features = extract_url_features("https://example.com")

    assert features["uses_https"] == 1
    assert features["has_ip_address"] == 0


def test_detects_ip_address_hostname():
    features = extract_url_features("http://192.168.1.10/login")

    assert features["has_ip_address"] == 1
    assert features["has_suspicious_keyword"] == 1


def test_counts_url_characters():
    features = extract_url_features("https://example.com/path?q=1")

    assert features["url_length"] == len(
        "https://example.com/path?q=1"
    )
    assert features["question_mark_count"] == 1
    assert features["equals_count"] == 1


def test_detects_punycode_hostname():
    features = extract_url_features("https://xn--example-ova.com")

    assert features["has_punycode"] == 1


@pytest.mark.parametrize("url", ["", "   ", None, 123])
def test_rejects_empty_or_invalid_input(url):
    with pytest.raises(ValueError):
        extract_url_features(url)
