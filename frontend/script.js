const API_URL = "http://127.0.0.1:8000/analyze";

let currentLanguage = "en";


/* =========================
   TRANSLATIONS
   ========================= */

const translations = {

    en: {
        subtitle: "Scam & Phishing Risk Checker",

        inputTitle: "Check a message or URL",
        inputDescription:
            "Paste a suspicious message, SMS, or URL below.",

        placeholder:
            "Paste your message or URL here...",

        analyze: "Analyze",
        analyzing: "Analyzing...",

        riskLabel: "RISK LEVEL",
        riskScore: "Risk Score",

        whyTitle: "Why was this flagged?",
        noIndicators:
            "No significant phishing indicators were detected.",

        domainTitle: "Domain Verification",

        submittedDomain: "Submitted domain:",
        officialDomain: "Official domain:",
        status: "Status:",

        safetyTitle: "Stay Safe",

        noActions:
            "Continue to stay cautious.",

        reset: "Check Another",

        connectionError:
            "Could not connect to the server. Please make sure FastAPI is running.",

        emptyInput:
            "Please enter a message or URL."
    },

    ta: {
        subtitle:
            "மோசடி மற்றும் ஃபிஷிங் ஆபத்து சரிபார்ப்பு",

        inputTitle:
            "செய்தி அல்லது URL-ஐ சரிபார்க்கவும்",

        inputDescription:
            "சந்தேகத்திற்கிடமான செய்தி, SMS அல்லது URL-ஐ கீழே உள்ளிடவும்.",

        placeholder:
            "உங்கள் செய்தி அல்லது URL-ஐ இங்கே உள்ளிடவும்...",

        analyze:
            "சரிபார்க்கவும்",

        analyzing:
            "சரிபார்க்கப்படுகிறது...",

        riskLabel:
            "ஆபத்து நிலை",

        riskScore:
            "ஆபத்து மதிப்பெண்",

        whyTitle:
            "இது ஏன் எச்சரிக்கப்பட்டது?",

        noIndicators:
            "குறிப்பிடத்தக்க ஃபிஷிங் குறிகாட்டிகள் எதுவும் கண்டறியப்படவில்லை.",

        domainTitle:
            "டொமைன் சரிபார்ப்பு",

        submittedDomain:
            "சமர்ப்பிக்கப்பட்ட டொமைன்:",

        officialDomain:
            "அதிகாரப்பூர்வ டொமைன்:",

        status:
            "நிலை:",

        safetyTitle:
            "பாதுகாப்பாக இருங்கள்",

        noActions:
            "தொடர்ந்து எச்சரிக்கையுடன் இருங்கள்.",

        reset:
            "மற்றொன்றை சரிபார்க்கவும்",

        connectionError:
            "சேவையகத்துடன் இணைக்க முடியவில்லை. FastAPI இயங்குகிறதா என்பதை சரிபார்க்கவும்.",

        emptyInput:
            "தயவுசெய்து ஒரு செய்தி அல்லது URL-ஐ உள்ளிடவும்."
    }
};


/* =========================
   LANGUAGE SWITCHING
   ========================= */

function setLanguage(language) {

    currentLanguage = language;

    const t = translations[language];

    document.getElementById("subtitle").textContent =
        t.subtitle;

    document.getElementById("inputTitle").textContent =
        t.inputTitle;

    document.getElementById("inputDescription").textContent =
        t.inputDescription;

    document.getElementById("messageInput").placeholder =
        t.placeholder;

    document.getElementById("analyzeBtn").textContent =
        t.analyze;

    document.getElementById("loadingText").textContent =
        t.analyzing;

    document.getElementById("riskLabel").textContent =
        t.riskLabel;

    document.getElementById("whyTitle").textContent =
        t.whyTitle;

    document.getElementById("domainTitle").textContent =
        t.domainTitle;

    document.getElementById("safetyTitle").textContent =
        t.safetyTitle;

    document.getElementById("resetBtn").textContent =
        t.reset;


    document.getElementById("englishBtn")
        .classList.toggle("active", language === "en");

    document.getElementById("tamilBtn")
        .classList.toggle("active", language === "ta");


    /*
     * If results are already visible,
     * refresh the dynamic text too.
     */
    const results =
        document.getElementById("results");

    if (!results.classList.contains("hidden")) {

        const riskLevel =
            results.dataset.riskLevel;

        const riskScore =
            results.dataset.riskScore;

        if (riskLevel !== undefined) {

            document.getElementById("riskLevel")
                .textContent =
                translateRiskLevel(riskLevel);
        }

        if (riskScore !== undefined) {

            document.getElementById("riskScore")
                .textContent =
                `${t.riskScore}: ${riskScore}`;
        }
    }
}


/* =========================
   ANALYZE MESSAGE
   ========================= */

async function analyzeMessage() {

    const input =
        document.getElementById("messageInput");

    const text =
        input.value.trim();


    if (!text) {

        alert(
            translations[currentLanguage].emptyInput
        );

        return;
    }


    const loading =
        document.getElementById("loading");

    const results =
        document.getElementById("results");

    const analyzeBtn =
        document.getElementById("analyzeBtn");


    loading.classList.remove("hidden");

    results.classList.add("hidden");

    analyzeBtn.disabled = true;


    try {

        const response = await fetch(
            API_URL,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    text: text
                })
            }
        );


        if (!response.ok) {
            throw new Error(
                "API request failed"
            );
        }


        const data =
            await response.json();


        displayResults(data);


    } catch (error) {

        console.error(error);

        alert(
            translations[currentLanguage]
                .connectionError
        );


    } finally {

        loading.classList.add("hidden");

        analyzeBtn.disabled = false;
    }
}


/* =========================
   DISPLAY RESULTS
   ========================= */

function displayResults(data) {

    const riskAnalysis =
        data.risk_analysis || {};

    const riskLevel =
        riskAnalysis.risk_level || "LOW RISK";

    const riskCard =
    document.querySelector(".risk-card");

riskCard.classList.remove(
    "risk-high",
    "risk-suspicious",
    "risk-low"
);

if (riskLevel === "HIGH RISK") {

    riskCard.classList.add("risk-high");

} else if (riskLevel === "SUSPICIOUS") {

    riskCard.classList.add("risk-suspicious");

} else {

    riskCard.classList.add("risk-low");
}

    const riskScore =
        riskAnalysis.risk_score ?? 0;


    const results =
        document.getElementById("results");


    /*
     * Store original English values.
     * This lets us switch language later.
     */

    results.dataset.riskLevel =
        riskLevel;

    results.dataset.riskScore =
        riskScore;


    document.getElementById("riskLevel")
        .textContent =
        translateRiskLevel(riskLevel);


    document.getElementById("riskScore")
        .textContent =
        `${translations[currentLanguage].riskScore}: ${riskScore}`;


    displayReasons(
        data.message_analysis,
        data.url_analysis,
        data.domain_verification
    );


    displayDomainVerification(
        data.domain_verification
    );


    displaySafeActions(
        data.safe_actions || []
    );


    results.classList.remove("hidden");


    results.scrollIntoView({
        behavior: "smooth"
    });
}


/* =========================
   RISK LEVEL TRANSLATION
   ========================= */

function translateRiskLevel(level) {

    if (currentLanguage === "ta") {

        if (level === "HIGH RISK") {
            return "அதிக ஆபத்து";
        }

        if (level === "SUSPICIOUS") {
            return "சந்தேகத்திற்கிடமானது";
        }

        if (level === "LOW RISK") {
            return "குறைந்த ஆபத்து";
        }
    }

    return level;
}


/* =========================
   REASONS
   ========================= */

function displayReasons(
    messageAnalysis,
    urlAnalysis,
    domainVerification
) {

    const list =
        document.getElementById("reasonsList");

    list.innerHTML = "";


    let reasons = [];


    /*
     * MESSAGE INDICATORS
     */

    if (messageAnalysis) {

        const indicators =
            messageAnalysis.indicators || [];


        indicators.forEach((indicator) => {

            if (indicator.type) {

                reasons.push(
                    currentLanguage === "ta"
                        ? translateIndicator(
                            indicator.type
                        )
                        : indicator.type
                );
            }
        });
    }


    /*
     * URL INDICATORS
     */

    if (urlAnalysis) {

        const urls =
            urlAnalysis.urls || [];


        urls.forEach((urlData) => {

            const indicators =
                urlData.indicators || [];


            indicators.forEach((indicator) => {

                if (indicator.name) {

                    reasons.push(
                        currentLanguage === "ta"
                            ? translateUrlIndicator(
                                indicator.name
                            )
                            : indicator.description
                    );
                }
            });
        });
    }


    /*
     * DOMAIN MISMATCH
     */

    if (
        domainVerification &&
        domainVerification.verification_status ===
            "MISMATCH"
    ) {

        reasons.push(
            currentLanguage === "ta"
                ? "சமர்ப்பிக்கப்பட்ட டொமைன் நிறுவனத்தின் அதிகாரப்பூர்வ டொமைனுடன் பொருந்தவில்லை."
                : "The submitted domain does not match the organization's verified official domain."
        );
    }


    /*
     * NO INDICATORS
     */

    if (reasons.length === 0) {

        const item =
            document.createElement("li");

        item.textContent =
            translations[currentLanguage]
                .noIndicators;

        list.appendChild(item);

        return;
    }


    /*
     * REMOVE DUPLICATES
     */

    reasons =
        [...new Set(reasons)];


    reasons.forEach((reason) => {

        const item =
            document.createElement("li");

        item.textContent = reason;

        list.appendChild(item);
    });
}


/* =========================
   DOMAIN VERIFICATION
   ========================= */

function displayDomainVerification(
    domainVerification
) {

    const section =
        document.getElementById(
            "domainSection"
        );

    const result =
        document.getElementById(
            "domainResult"
        );


    result.innerHTML = "";


    if (!domainVerification) {

        section.classList.add("hidden");

        return;
    }


    const status =
        domainVerification
            .verification_status;


    if (!status) {

        section.classList.add("hidden");

        return;
    }


    section.classList.remove("hidden");


    const submittedDomain =
        domainVerification.submitted_domain ||
        "Unknown";


    const officialDomain =
        domainVerification.official_domain ||
        "Unknown";


    const t =
        translations[currentLanguage];


    const statusText =
        translateDomainStatus(status);


    result.innerHTML = `

        <div class="domain-result">

            <div>
                <strong>
                    ${t.submittedDomain}
                </strong>

                ${submittedDomain}
            </div>


            <div>
                <strong>
                    ${t.officialDomain}
                </strong>

                ${officialDomain}
            </div>


            <div class="domain-status">

                <strong>
                    ${t.status}
                </strong>

                ${statusText}

            </div>

        </div>
    `;
}


function translateDomainStatus(status) {

    if (currentLanguage === "ta") {

        if (status === "MATCH") {
            return "✓ பொருந்துகிறது";
        }

        if (status === "MISMATCH") {
            return "✗ பொருந்தவில்லை";
        }

        return "தெரியவில்லை";
    }


    if (status === "MATCH") {
        return "✓ MATCH";
    }

    if (status === "MISMATCH") {
        return "✗ MISMATCH";
    }

    return status;
}


/* =========================
   SAFE ACTIONS
   ========================= */

function displaySafeActions(actions) {

    const list =
        document.getElementById(
            "actionsList"
        );


    list.innerHTML = "";


    if (actions.length === 0) {

        const item =
            document.createElement("li");

        item.textContent =
            translations[currentLanguage]
                .noActions;

        list.appendChild(item);

        return;
    }


    actions.forEach((action) => {

        const item =
            document.createElement("li");


        item.textContent =
            currentLanguage === "ta"
                ? translateSafetyAction(action)
                : action;


        list.appendChild(item);
    });
}


/* =========================
   INDICATOR TRANSLATIONS
   ========================= */

function translateIndicator(indicator) {

    const translationsTamil = {

        "Reward or lure-based claim":
            "வெகுமதி அல்லது பரிசு வழங்குவதாகக் கூறுகிறது",

        "Payment or fee request":
            "பணம் அல்லது கட்டணம் செலுத்துமாறு கேட்கிறது",

        "Urgency or pressure":
            "அவசரமாக நடவடிக்கை எடுக்க அழுத்தம் கொடுக்கிறது",

        "Fear or threat-based language":
            "பயம் அல்லது அச்சுறுத்தலை ஏற்படுத்தும் மொழியைப் பயன்படுத்துகிறது",

        "Organization impersonation":
            "ஒரு நிறுவனத்தைப் போல ஆள்மாறாட்டம் செய்கிறது",

        "OTP or credential request":
            "OTP அல்லது உள்நுழைவு தகவலைக் கேட்கிறது",

        "Account or KYC verification":
            "கணக்கு அல்லது KYC சரிபார்ப்பைக் கோருகிறது"
    };


    return (
        translationsTamil[indicator] ||
        indicator
    );
}


/* =========================
   URL TRANSLATIONS
   ========================= */

function translateUrlIndicator(name) {

    const translationsTamil = {

        suspicious_tld:
            "டொமைன் சந்தேகத்திற்கிடமான TLD-ஐ பயன்படுத்துகிறது",

        ip_address:
            "URL ஒரு டொமைன் பெயருக்கு பதிலாக IP முகவரியைப் பயன்படுத்துகிறது",

        excessive_subdomains:
            "டொமைனில் வழக்கத்திற்கு மாறாக அதிகமான subdomains உள்ளன",

        encoded_url:
            "URL-ல் encoded characters உள்ளன",

        at_symbol:
            "URL-ல் உண்மையான இலக்கை மறைக்கக்கூடிய '@' குறியீடு உள்ளது",

        shortened_url:
            "URL shortening சேவை பயன்படுத்தப்பட்டுள்ளது",

        long_url:
            "URL வழக்கத்திற்கு மாறாக நீளமாக உள்ளது"
    };


    return (
        translationsTamil[name] ||
        name
    );
}


/* =========================
   SAFETY TRANSLATIONS
   ========================= */

function translateSafetyAction(action) {

    const translationsTamil = {

        "Do not click suspicious links or follow instructions in the message.":
            "சந்தேகத்திற்கிடமான இணைப்புகளை கிளிக் செய்யாதீர்கள் அல்லது செய்தியில் உள்ள வழிமுறைகளைப் பின்பற்றாதீர்கள்.",

        "Do not make payments or pay fees requested through the message.":
            "செய்தி மூலம் கோரப்படும் பணம் அல்லது கட்டணத்தை செலுத்தாதீர்கள்.",

        "Avoid entering personal or financial information through the submitted link.":
            "சமர்ப்பிக்கப்பட்ட இணைப்பில் தனிப்பட்ட அல்லது நிதித் தகவல்களை உள்ளிடுவதைத் தவிர்க்கவும்.",

        "Verify the organization independently using its official website or app.":
            "நிறுவனத்தின் அதிகாரப்பூர்வ இணையதளம் அல்லது செயலியைப் பயன்படுத்தி நிறுவனத்தைத் தனியாகச் சரிபார்க்கவும்.",

        "Never share OTPs, passwords, PINs, or other sensitive credentials.":
            "OTP, கடவுச்சொல், PIN அல்லது பிற முக்கியமான தகவல்களை யாருடனும் பகிர வேண்டாம்.",

        "Be cautious before clicking links or sharing any information.":
            "இணைப்புகளை கிளிக் செய்வதற்கு முன்பும் தகவல்களைப் பகிர்வதற்கு முன்பும் எச்சரிக்கையுடன் இருங்கள்.",

        "No strong phishing indicators were detected, but remain cautious.":
            "வலுவான ஃபிஷிங் குறிகாட்டிகள் கண்டறியப்படவில்லை. இருப்பினும் தொடர்ந்து எச்சரிக்கையுடன் இருங்கள்."
    };


    return (
        translationsTamil[action] ||
        action
    );
}


/* =========================
   RESET
   ========================= */

function resetAnalysis() {

    document.getElementById(
        "messageInput"
    ).value = "";


    document.getElementById(
        "results"
    ).classList.add("hidden");


    document.getElementById(
        "domainSection"
    ).classList.add("hidden");


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}