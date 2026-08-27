def verify_domain(
    organization_analysis: dict,
    url_analysis: dict
) -> dict:
    """
    Compare detected organization trusted domains
    against the actual domains found in URLs.
    """

    organizations = organization_analysis.get("organizations", [])
    urls = url_analysis.get("urls", [])

    results = []

    # Nothing to verify
    if not organizations:
        return {
            "verification_status": "NOT_APPLICABLE",
            "results": []
        }

    # Organization detected but no URL
    if not urls:
        return {
            "verification_status": "NO_URL",
            "results": []
        }

    for organization in organizations:

        organization_name = organization.get("name")
        trusted_domains = organization.get("trusted_domains", [])

        for url in urls:

            actual_domain = url.get("domain", "").lower()

            matched = actual_domain in [
                domain.lower()
                for domain in trusted_domains
            ]

            if matched:
                status = "MATCH"
                explanation = (
                    f"The URL domain matches a trusted domain "
                    f"for {organization_name}."
                )
            else:
                status = "MISMATCH"
                explanation = (
                    f"The URL domain does not match any trusted "
                    f"domain for {organization_name}."
                )

            results.append({
                "organization": organization_name,
                "actual_domain": actual_domain,
                "trusted_domains": trusted_domains,
                "status": status,
                "explanation": explanation
            })

    overall_status = (
        "MATCH"
        if all(result["status"] == "MATCH" for result in results)
        else "MISMATCH"
    )

    return {
        "verification_status": overall_status,
        "results": results
    }