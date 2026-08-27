RISK_LEVELS = {
    "LOW RISK": {
        "minimum_score": 0,
    },
    "SUSPICIOUS": {
        "minimum_score": 4,
    },
    "HIGH RISK": {
        "minimum_score": 8,
    },
}


def calculate_risk(
    message_analysis: dict,
    url_analysis: dict
) -> dict:
    """
    Combine message and URL evidence into a preliminary
    unified risk assessment.
    """

    message_score = message_analysis.get("total_score", 0)

    url_score = sum(
        url.get("score", 0)
        for url in url_analysis.get("urls", [])
    )

    total_score = message_score + url_score

    if total_score >= RISK_LEVELS["HIGH RISK"]["minimum_score"]:
        risk_level = "HIGH RISK"

    elif total_score >= RISK_LEVELS["SUSPICIOUS"]["minimum_score"]:
        risk_level = "SUSPICIOUS"

    else:
        risk_level = "LOW RISK"

    reasons = []

    # Message-based reasons
    for indicator in message_analysis.get("indicators", []):
        reasons.append(indicator.get("type"))

    # URL-based reasons
    for url in url_analysis.get("urls", []):
        for indicator in url.get("indicators", []):
            reasons.append(indicator.get("description"))

    return {
        "risk_level": risk_level,
        "risk_score": total_score,
        "message_score": message_score,
        "url_score": url_score,
        "reasons": reasons,
    }