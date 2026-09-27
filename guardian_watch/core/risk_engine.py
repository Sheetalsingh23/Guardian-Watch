from __future__ import annotations

from typing import Iterable

from guardian_watch.core.schemas import AgentResult


def normalize_status(status: str) -> str:
    status = (status or "").lower()
    if status in {"urgent", "emergency"}:
        return "urgent"
    if status in {"review", "high"}:
        return "review"
    if status in {"monitor", "moderate"}:
        return "monitor"
    return "low"


def determine_final_status(agent_results: Iterable[AgentResult]) -> tuple[str, str]:
    results = list(agent_results)
    if any(result.status == "urgent" for result in results):
        return "urgent", "Immediate medical attention recommended"

    review_count = sum(1 for result in results if normalize_status(result.status) == "review")
    monitor_count = sum(1 for result in results if normalize_status(result.status) == "monitor")

    if review_count >= 2:
        return "review", "Multiple related concerns detected"
    if review_count == 1 or monitor_count >= 2:
        return "monitor", "One or more concerning observations were reported"
    if any(result.requires_human_review for result in results):
        return "monitor", "Monitor and consider routine professional review"
    return "low", "No significant concern detected from the provided information"


def describe_risk_summary(status: str, findings_count: int) -> str:
    if status == "urgent":
        return "Urgent medical review recommended"
    if status == "review":
        return f"Review recommended — {findings_count} related concerns detected."
    if status == "monitor":
        return f"Monitor — {findings_count} concerns identified."
    return "Low concern — continue monitoring."
