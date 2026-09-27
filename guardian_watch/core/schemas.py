from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class Finding:
    factor: str
    evidence: str

    def to_dict(self) -> dict[str, str]:
        return {"factor": self.factor, "evidence": self.evidence}


@dataclass
class AgentResult:
    agent: str
    status: str
    findings: List[Finding] = field(default_factory=list)
    confidence: str = "moderate"
    requires_human_review: bool = False
    recommendation: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent": self.agent,
            "status": self.status,
            "findings": [item.to_dict() for item in self.findings],
            "confidence": self.confidence,
            "requires_human_review": self.requires_human_review,
            "recommendation": self.recommendation,
        }


@dataclass
class ElderContext:
    elder_name: str = "Elder"
    age: int = 75
    daily_routine: str = ""
    medications: str = ""
    recent_changes: str = ""
    mobility: str = ""
    home_factors: str = ""
    behavioral_changes: str = ""
    recent_falls: str = ""
    baseline_routine: str = ""

    def as_text(self) -> str:
        return "\n".join(
            [
                self.daily_routine,
                self.medications,
                self.recent_changes,
                self.mobility,
                self.home_factors,
                self.behavioral_changes,
                self.recent_falls,
                self.baseline_routine,
            ]
        )
