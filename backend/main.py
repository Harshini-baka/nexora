from fastapi import FastAPI
from pydantic import BaseModel

from backend.services.message_analyzer import analyze_message
from backend.services.risk_engine import calculate_risk
from backend.services.url_analyzer import analyze_urls
from backend.services.organization_detector import detect_organization
from backend.services.domain_verifier import verify_domain

app = FastAPI()


class AnalyzeRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {
        "message": "Welcome to Nexora API"
    }


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    message_analysis = analyze_message(request.text)

    url_analysis = analyze_urls(request.text)

    organization_analysis = detect_organization(
        request.text
    )

    domain_verification = verify_domain(
        organization_analysis,
        url_analysis
    )

    risk_analysis = calculate_risk(
        message_analysis,
        url_analysis,
        domain_verification
    )

    return {
        "input": request.text,
        "message_analysis": message_analysis,
        "url_analysis": url_analysis,
        "organization_analysis": organization_analysis,
        "domain_verification": domain_verification,
        "risk_analysis": risk_analysis
    }