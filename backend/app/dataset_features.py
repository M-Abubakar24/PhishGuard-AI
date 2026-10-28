
from collections import Counter
from math import log2
from urllib.parse import urlparse
import ipaddress

import tldextract


def extract_dataset_features(url: str) -> dict:
    """Extract the numerical features used by the PhishGuard training dataset."""

    url = url.strip()
    if not url:
        raise ValueError("URL cannot be empty.")

    # Parse consistently even when the user omits the scheme.
    candidate = url if "://" in url else f"http://{url}"
    parsed = urlparse(candidate)
    hostname = (parsed.hostname or "").lower()

    if not hostname:
        raise ValueError("Please provide a valid URL with a hostname.")

    try:
        ipaddress.ip_address(hostname)
        is_ip = 1
    except ValueError:
        is_ip = 0

    extracted = tldextract.extract(hostname)
    domain = extracted.top_domain_under_public_suffix or hostname
    tld = extracted.suffix

    # Count subdomains preceding the registered domain.
    subdom_cnt = (
        len(extracted.subdomain.split("."))
        if extracted.subdomain
        else 0
    )

    letters = sum(ch.isalpha() for ch in url)
    digits = sum(ch.isdigit() for ch in url)
    special = sum(not ch.isalnum() for ch in url)
    length = len(url)

    # Shannon entropy over URL characters.
    counts = Counter(url)
    entropy = -sum(
        (count / length) * log2(count / length)
        for count in counts.values()
    ) if length else 0.0

    return {
        "url_len": length,
        "dom_len": len(domain),
        "is_ip": is_ip,
        "tld_len": len(tld),
        "subdom_cnt": subdom_cnt,
        "letter_cnt": letters,
        "digit_cnt": digits,
        "special_cnt": special,
        "eq_cnt": url.count("="),
        "qm_cnt": url.count("?"),
        "amp_cnt": url.count("&"),
        "dot_cnt": url.count("."),
        "dash_cnt": url.count("-"),
        "under_cnt": url.count("_"),
        "letter_ratio": letters / length if length else 0.0,
        "digit_ratio": digits / length if length else 0.0,
        "spec_ratio": special / length if length else 0.0,
        "is_https": int(parsed.scheme.lower() == "https"),
        "slash_cnt": url.count("/"),
        "entropy": entropy,
        "path_len": len(parsed.path),
        "query_len": len(parsed.query),
    }
