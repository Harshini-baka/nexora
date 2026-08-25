from fastapi import FastAPI
from pydantic import BaseModel

from backend.services.message_analyzer import analyze_message
from backend.services.risk_engine import calculate_risk

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
    risk_analysis = calculate_risk(message_analysis)

    return {
        "input": request.text,
        "message_analysis": message_analysis,
        "risk_analysis": risk_analysis
    }