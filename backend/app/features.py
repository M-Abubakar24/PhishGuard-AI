
import ipaddress
import re
from urllib.parse import urlparse


SUSPICIOUS_KEYWORDS = {
    "login",
    "verify",
    "verification",
    "account",
    "secure",
    "update",
    "password",
    "signin",
    "confirm",
    "wallet",
    "banking",
    "suspend",
    "recover",
}


def extract_url_features(url: str) -> dict:
    """
    Extract measurable URL features for phishing detection.

    These features are signals for a machine-learning model, not
    proof that a URL is malicious or safe.
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string.")

    url = url.strip()

    # Parse the URL safely, even if the scheme is missing.
    candidate = url if "://" in url else f"//{url}"
    parsed = urlparse(candidate)

    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    if not hostname:
        raise ValueError("URL must contain a valid hostname.")

    # Detect whether the hostname is an IPv4 or IPv6 address.
    try:
        ipaddress.ip_address(hostname)
        has_ip_address = 1
    except ValueError:
        has_ip_address = 0

    hostname_parts = hostname.split(".")
    registered_domain_candidate = (
        hostname_parts[-2] if len(hostname_parts) >= 2 else hostname
    )

    hostname_lower = hostname.lower()
    url_lower = url.lower()

    features = {
        "url_length": len(url),
        "hostname_length": len(hostname),
        "path_length": len(path),
        "query_length": len(query),
        "dot_count": url.count("."),
        "hyphen_count": url.count("-"),
        "at_symbol_count": url.count("@"),
        "question_mark_count": url.count("?"),
        "equals_count": url.count("="),
        "ampersand_count": url.count("&"),
        "percent_count": url.count("%"),
        "slash_count": url.count("/"),
        "digit_count": sum(char.isdigit() for char in url),
        "has_ip_address": has_ip_address,
        "uses_https": int(parsed.scheme.lower() == "https"),
        "has_nonstandard_port": int(
            _has_nonstandard_port(parsed)
        ),
        "subdomain_count": max(len(hostname_parts) - 2, 0),
        "has_punycode": int("xn--" in hostname_lower),
        "has_double_slash_in_path": int("//" in path),
        "has_suspicious_keyword": int(
            any(keyword in url_lower for keyword in SUSPICIOUS_KEYWORDS)
        ),
        "hostname_has_hyphen": int("-" in hostname_lower),
        "hostname_is_local_or_single_label": int(
            "." not in hostname_lower
        ),
        "hostname_length_excluding_dots": len(
            hostname_lower.replace(".", "")
        ),
        "domain_candidate_length": len(registered_domain_candidate),
        "has_encoded_characters": int(bool(re.search(r"%[0-9a-fA-F]{2}", url))),
    }

    return features


def _has_nonstandard_port(parsed) -> bool:
    """Return True when a URL specifies a port other than 80 or 443."""
    try:
        port = parsed.port
    except ValueError:
        return True

    return port is not None and port not in (80, 443)
