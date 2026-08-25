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


def calculate_risk(message_analysis: dict) -> dict:
    """
    Convert message-analysis evidence into a preliminary risk assessment.

    This is the message-only risk engine for now.
    URL and domain evidence will be added later.
    """

    total_score = message_analysis.get("total_score", 0)

    if total_score >= RISK_LEVELS["HIGH RISK"]["minimum_score"]:
        risk_level = "HIGH RISK"
    elif total_score >= RISK_LEVELS["SUSPICIOUS"]["minimum_score"]:
        risk_level = "SUSPICIOUS"
    else:
        risk_level = "LOW RISK"

    return {
        "risk_level": risk_level,
        "risk_score": total_score,
    }