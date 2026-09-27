from __future__ import annotations

from guardian_watch.core.schemas import AgentResult, Finding


def cross_check(results: list[AgentResult]) -> AgentResult:
    factors = []
    labels = {"fall_risk": "fall risk", "medication_risk": "medication concern", "change_detection": "pattern change"}

    for result in results:
        if result.agent in labels and result.status in {"monitor", "review", "urgent"}:
            for finding in result.findings:
                factors.append(finding.factor)

    if not factors:
        return AgentResult(
            agent="cross_check",
            status="low",
            findings=[Finding("no_cross_check_signal", "No related concerns were connected across agents.")],
            confidence="low",
            requires_human_review=False,
            recommendation="No linked risk pattern identified from the current information.",
        )

    status = "monitor"
    if sum(1 for result in results if result.status in {"review", "urgent"}) >= 2:
        status = "review"

    return AgentResult(
        agent="cross_check",
        status=status,
        findings=[Finding("linked_pattern", "Reported mobility, dizziness, and recent medication or routine changes overlap in time.")],
        confidence="moderate",
        requires_human_review=True,
        recommendation="The reported timing of medication or routine changes with dizziness or mobility concerns may warrant professional review.",
    )
