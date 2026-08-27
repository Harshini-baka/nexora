ORGANIZATION_DOMAINS = {
    "sbi": {
        "name": "State Bank of India",
        "domains": ["sbi.co.in"],
    },
    "hdfc": {
        "name": "HDFC Bank",
        "domains": ["hdfcbank.com"],
    },
    "icici": {
        "name": "ICICI Bank",
        "domains": ["icicibank.com"],
    },
    "axis": {
        "name": "Axis Bank",
        "domains": ["axisbank.com"],
    },
    "amazon": {
        "name": "Amazon",
        "domains": ["amazon.in", "amazon.com"],
    },
    "flipkart": {
        "name": "Flipkart",
        "domains": ["flipkart.com"],
    },
}


def detect_organization(text: str) -> dict:
    """
    Detect organizations mentioned in a message.

    This is an initial rule-based implementation.
    """

    text_lower = text.lower()

    detected = []

    for keyword, organization in ORGANIZATION_DOMAINS.items():

        if keyword in text_lower:

            detected.append({
                "keyword": keyword,
                "name": organization["name"],
                "trusted_domains": organization["domains"],
            })

    return {
        "organization_count": len(detected),
        "organizations": detected,
    }