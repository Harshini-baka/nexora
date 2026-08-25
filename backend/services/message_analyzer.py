import re

NEGATION_PATTERNS = [
    r"\bnever\s+(share|send|provide|give|tell|forward)\b",
    r"\bdo not\s+(share|send|provide|give|tell|forward)\b",
    r"\bdon['’]?t\s+(share|send|provide|give|tell|forward)\b",
    r"\bavoid\s+(sharing|sending|providing|giving)\b",
]

PATTERNS = {
    "urgency": [
        {
            "pattern": r"\b(act now|immediately|urgent|urgently|asap|hurry)\b",
            "score": 3,
            "description": "Strong pressure to act immediately",
        },
        {
            "pattern": r"\b(today|now|expires?|expiring)\b",
            "score": 1,
            "description": "Time-sensitive language",
        },
        {
            "pattern": r"\b(don['’]?t miss|limited time|last chance|final chance|act quickly|hurry|before it expires)\b",
            "score": 2,
            "description": "Pressure to avoid missing an opportunity",
        },
    ],

    "fear_or_threat": [
        {
            "pattern": r"\b(account will be blocked|account will be suspended|legal action|penalty|fine)\b",
            "score": 3,
            "description": "Threat or consequence used to pressure the user",
        },
        {
            "pattern": r"\b(blocked|suspended|terminated|locked|warning|violation)\b",
            "score": 1,
            "description": "Potentially threatening language",
        },
    ],

    "reward_or_lure": [
        {
            "pattern": r"\b(congratulations?).{0,50}\b(won|winner).{0,30}\b(prize|reward|cash|bonus)\b",
            "score": 3,
            "description": "Claim of winning a reward or prize",
        },
        {
            "pattern": r"\b(exclusive|special|limited|cash|mega|grand).{0,20}\b(prize|reward|bonus|offer)\b",
            "score": 2,
            "description": "Promotional reward or prize lure",
        },
        {
            "pattern": r"\b(cash|money|monetary).{0,20}\b(prize|reward|bonus|offer)\b",
            "score": 2,
            "description": "Cash-based reward lure",
        },
        {
            "pattern": r"\b(claim|collect|win|won).{0,30}\b(your|the|a|our)?\s*(prize|reward|cash|bonus|gift)\b",
            "score": 2,
            "description": "Invitation to obtain a reward",
        },
        {
            "pattern": r"\b(test your luck|try your luck|lucky chance|lucky draw|lucky winner)\b",
            "score": 2,
            "description": "Luck-based promotional lure",
        },
    ],

    "otp_or_credentials": [
        {
            "pattern": r"\b(share|send|provide|give|tell|forward).{0,20}\b(otp|one[- ]time password)\b",
            "score": 4,
            "description": "Request to provide an OTP",
        },
        {
            "pattern": r"\b(share|send|provide|give|tell|forward).{0,20}\b(password|passcode|pin|cvv|credentials?)\b",
            "score": 4,
            "description": "Request for sensitive credentials",
        },
        {
            "pattern": r"\b(enter|input|type).{0,20}\b(otp|one[- ]time password)\b",
            "score": 2,
            "description": "Instruction to enter an OTP",
        },
    ],

    "account_or_kyc_verification": [
        {
            "pattern": r"\b(verify|update|confirm).{0,30}\b(your )?(account|kyc|identity)\b",
            "score": 2,
            "description": "Account or identity verification request",
        },
        {
            "pattern": r"\b(kyc|know your customer)\b",
            "score": 1,
            "description": "KYC-related language",
        },
    ],

    "payment_or_fee_request": [
        {
            "pattern": r"\b(pay|payment|send|transfer).{0,30}\b(fee|charge|deposit|amount|money|₹|\$|rs\.?)\b",
            "score": 3,
            "description": "Request for payment or money",
        },
        {
            "pattern": r"\b(pay|send|transfer)\s+(₹|\$|rs\.?)?\s*\d[\d,]*(?:\.\d+)?\b",
            "score": 4,
            "description": "Direct request to pay a specific amount",
        },
        {
            "pattern": r"\b(registration|register|processing|verification|entry).{0,30}\b(fee|payment|charge|amount)\b",
            "score": 3,
            "description": "Payment associated with registration or access",
        },
        {
            "pattern": r"\b(verification fee|processing fee|registration fee|entry fee|refund fee)\b",
            "score": 3,
            "description": "Specific fee request",
        },
    ],

    "organization_reference": [
        {
            "pattern": r"\b(bank|government|police|income tax|rbi|sbi|hdfc|icici|amazon|flipkart|google)\b",
            "score": 1,
            "description": "Organization or authority mentioned",
        },
    ],
}

SAFETY_PATTERNS = [
    r"\bdon['’]?t share\b",
    r"\bdo not share\b",
    r"\bnever share\b",
    r"\bkeep (it|this) private\b",
    r"\bkeep (it|this) confidential\b",
]

INDICATOR_NAMES = {
    "urgency": "Urgency and pressure",
    "fear_or_threat": "Fear or threat-based language",
    "reward_or_lure": "Reward or lure-based claim",
    "otp_or_credentials": "OTP or credential request",
    "account_or_kyc_verification": "Account or KYC verification request",
    "payment_or_fee_request": "Payment or fee request",
    "organization_reference": "Organization or authority reference",
}

def has_negated_credential_instruction(text: str) -> bool:
    """
    Detects security advice that explicitly tells the user
    NOT to share sensitive information.
    """

    return any(
        re.search(pattern, text, flags=re.IGNORECASE)
        for pattern in NEGATION_PATTERNS
    )

def analyze_message(text: str) -> dict:
    """
    Analyze message content and extract weighted phishing evidence.

    This function does NOT decide whether the message is phishing.
    It only produces evidence for the Risk Engine.
    """
    negated_credential_instruction = has_negated_credential_instruction(text)
    detected_indicators = []

    safety_context = any(
    re.search(pattern, text, flags=re.IGNORECASE)
    for pattern in SAFETY_PATTERNS
)


    for indicator, rules in PATTERNS.items():
        if indicator == "otp_or_credentials" and negated_credential_instruction:
            continue

        indicator_score = 0
        evidence = []
        descriptions = []

        for rule in rules:
            matches = re.findall(
                rule["pattern"],
                text,
                flags=re.IGNORECASE
            )

            if matches:
                indicator_score += rule["score"]

                for match in matches:
                    if isinstance(match, tuple):
                        match = " ".join(match)

                    if match not in evidence:
                        evidence.append(match)

                if rule["description"] not in descriptions:
                    descriptions.append(rule["description"])

        if evidence:
            if indicator_score >= 4:
                strength = "strong"
            elif indicator_score >= 2:
                strength = "moderate"
            else:
                strength = "weak"

            detected_indicators.append(
                {
                    "type": INDICATOR_NAMES[indicator],
                    "strength": strength,
                    "score": indicator_score,
                    "evidence": evidence,
                    "explanation": descriptions,
                }
            )

    total_score = sum(
        indicator["score"]
        for indicator in detected_indicators
    )

    return {
        "total_score": total_score,
        "indicator_count": len(detected_indicators),
        "indicators": detected_indicators,
    }