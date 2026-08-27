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
    url_analysis: dict,
    domain_verification: dict
) -> dict:
    """
    Combine message, URL, and domain-verification evidence
    into a unified risk assessment.
    """

    message_score = message_analysis.get("total_score", 0)

    url_score = sum(
        url.get("score", 0)
        for url in url_analysis.get("urls", [])
    )

    # Domain verification score
    domain_score = 0

    if domain_verification.get("verification_status") == "MISMATCH":
        domain_score = 4

    total_score = (
        message_score
        + url_score
        + domain_score
    )

    if total_score >= RISK_LEVELS["HIGH RISK"]["minimum_score"]:
        risk_level = "HIGH RISK"

    elif total_score >= RISK_LEVELS["SUSPICIOUS"]["minimum_score"]:
        risk_level = "SUSPICIOUS"

    else:
        risk_level = "LOW RISK"

    reasons = []

    # Message reasons
    for indicator in message_analysis.get("indicators", []):
        reasons.append(indicator.get("type"))

    # URL reasons
    for url in url_analysis.get("urls", []):
        for indicator in url.get("indicators", []):
            reasons.append(indicator.get("description"))

    # Domain verification reason
    if domain_verification.get("verification_status") == "MISMATCH":
        reasons.append(
            "Submitted URL domain does not match the trusted domain "
            "of the detected organization"
        )

    return {
        "risk_level": risk_level,
        "risk_score": total_score,
        "message_score": message_score,
        "url_score": url_score,
        "domain_score": domain_score,
        "reasons": reasons,
    }