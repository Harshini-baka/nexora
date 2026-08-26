import re
from urllib.parse import urlparse


# URL patterns that can be extracted from a message
URL_PATTERN = r"https?://[^\s]+"

# Initial suspicious TLD list.
# This is a heuristic, NOT proof that a URL is malicious.
SUSPICIOUS_TLDS = {
    ".xyz",
    ".top",
    ".click",
    ".link",
    ".work",
    ".zip",
}

# Common URL shorteners
SHORTENER_DOMAINS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "is.gd",
    "cutt.ly",
    "shorturl.at",
}


def extract_urls(text: str) -> list[str]:
    """
    Extract HTTP/HTTPS URLs from a message.
    """

    return re.findall(URL_PATTERN, text)


def is_ip_address(domain: str) -> bool:
    """
    Check whether the hostname is an IPv4 address.
    """
    return bool(
        re.fullmatch(
            r"(?:\d{1,3}\.){3}\d{1,3}",
            domain
        )
    )


def has_suspicious_tld(domain: str) -> bool:
    """
    Check whether the domain uses one of our initial
    suspicious-TLD heuristics.
    """

    return any(
        domain.endswith(tld)
        for tld in SUSPICIOUS_TLDS
    )


def has_excessive_subdomains(domain: str) -> bool:
    """
    Detect unusually deep subdomain structures.

    Example:
    login.verify.account.example.com
    """

    parts = domain.split(".")

    return len(parts) >= 5


def has_encoded_characters(url: str) -> bool:
    """
    Detect percent-encoded characters in a URL.
    """

    return bool(re.search(r"%[0-9A-Fa-f]{2}", url))


def has_suspicious_at_symbol(url: str) -> bool:
    """
    Detect '@' in a URL.

    In URLs such as:

    https://trusted.com@evil.com/login

    the actual hostname is evil.com.
    """

    return "@" in url


def is_shortened_url(domain: str) -> bool:
    """
    Detect common URL-shortening services.
    """

    return domain in SHORTENER_DOMAINS


def analyze_url(url: str) -> dict:
    """
    Analyze one URL and return explainable evidence.

    This function does NOT decide whether the URL is a scam.
    It only extracts suspicious characteristics.
    """

    parsed = urlparse(url)

    domain = parsed.hostname or ""
    domain = domain.lower()

    indicators = []
    score = 0

   

    if is_ip_address(domain):
        indicators.append({
            "name": "ip_address",
            "description": "URL uses an IP address instead of a domain name",
            "score": 2,
        })
        score += 2


    if has_suspicious_tld(domain):
        indicators.append({
            "name": "suspicious_tld",
            "description": "Domain uses a potentially suspicious top-level domain",
            "score": 2,
        })
        score += 2

   
    if has_excessive_subdomains(domain):
        indicators.append({
            "name": "excessive_subdomains",
            "description": "Domain contains an unusually large number of subdomains",
            "score": 2,
        })
        score += 2

    
    if has_encoded_characters(url):
        indicators.append({
            "name": "encoded_url",
            "description": "URL contains percent-encoded characters",
            "score": 1,
        })
        score += 1


    if has_suspicious_at_symbol(url):
        indicators.append({
            "name": "at_symbol",
            "description": "URL contains '@', which can obscure the actual destination",
            "score": 3,
        })
        score += 3

   
    if is_shortened_url(domain):
        indicators.append({
            "name": "shortened_url",
            "description": "URL uses a URL-shortening service",
            "score": 2,
        })
        score += 2

    
    if len(url) > 150:
        indicators.append({
            "name": "long_url",
            "description": "URL is unusually long",
            "score": 1,
        })
        score += 1

    return {
        "url": url,
        "domain": domain,
        "uses_https": parsed.scheme.lower() == "https",
        "url_length": len(url),
        "score": score,
        "indicators": indicators,
    }


def analyze_urls(text: str) -> dict:
    """
    Extract and analyze all URLs found in a message.
    """

    urls = extract_urls(text)

    analyzed_urls = [
        analyze_url(url)
        for url in urls
    ]

    return {
        "url_count": len(analyzed_urls),
        "urls": analyzed_urls,
    }