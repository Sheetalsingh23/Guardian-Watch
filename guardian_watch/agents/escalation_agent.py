from __future__ import annotations

from guardian_watch.core.schemas import AgentResult, Finding


def create_escalation(status: str, findings_count: int) -> AgentResult:
    if status == "urgent":
        return AgentResult(
            agent="escalation",
            status="urgent",
            findings=[Finding("immediate_attention", "Emergency warning signs were reported.")],
            confidence="high",
            requires_human_review=True,
            recommendation="Seek immediate emergency care and contact emergency services as needed.",
        )

    if status == "review":
        return AgentResult(
            agent="escalation",
            status="review",
            findings=[Finding("professional_review", f"{findings_count} related concerns detected; professional review is recommended.")],
            confidence="moderate",
            requires_human_review=True,
            recommendation="Contact the elder's healthcare professional or pharmacist to review mobility, medications, and recent changes.",
        )

    return AgentResult(
        agent="escalation",
        status="monitor",
        findings=[Finding("routine_follow_up", "No urgent issues were detected from the current screening.")],
        confidence="low",
        requires_human_review=False,
        recommendation="Continue monitoring and update the care team if the pattern changes.",
    )
