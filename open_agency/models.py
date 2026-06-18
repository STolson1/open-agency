"""The request and the decision.

`Decision` is the `Option[Rejection]` made concrete: a denial is the unmarked
default a request has to argue its way out of, and any approval has to cite the
clause that permits it.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Plea(BaseModel):
    """An employee request."""

    plea: str = Field(..., description="The employee's request or question, in their words.")
    context: dict | None = Field(
        default=None,
        description="Optional structured context (role, tenure, location, etc.).",
    )


class DecisionType(str, Enum):
    approved = "approved"
    denied = "denied"
    needs_more_info = "needs_more_info"


class Decision(BaseModel):
    """The HR representative's answer."""

    decision: DecisionType = Field(..., description="The outcome.")
    message: str = Field(..., description="The reply to the employee, in an HR voice.")
    policy_basis: list[str] = Field(
        default_factory=list,
        description="The specific policy clauses the decision rests on.",
    )
