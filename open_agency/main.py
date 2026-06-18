"""FastAPI app. One endpoint that matters: POST /request."""

from __future__ import annotations

from fastapi import FastAPI

from .config import get_settings
from .hr_agent import HRAgent
from .models import Decision, Plea

settings = get_settings()
agent = HRAgent(settings)

app = FastAPI(
    title="Open Agency — HR request API",
    version="0.1.0",
    description="One verb. It consults written policy and usually says no.",
)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "model": settings.model,
        "effort": settings.effort,
        "company": settings.company_name,
    }


@app.post("/request", response_model=Decision)
def request(plea: Plea) -> Decision:
    """Submit a request. Get a policy-grounded decision back."""
    return agent.decide(plea.plea, plea.context)
