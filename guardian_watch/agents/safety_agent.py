from __future__ import annotations

from guardian_watch.core.schemas import AgentResult, Finding


def evaluate_safety(context_text: str) -> AgentResult:
    text = context_text.lower()
    emergency_words = [
        "unconscious",
        "seizing",
        "chest pain",
        "trouble breathing",
        "cannot wake",
        "severe bleeding",
        "stroke",
        "heart attack",
        "passed out",
        "lost consciousness",
        "collapsed",
    ]
    if any(word in text for word in emergency_words):
        return AgentResult(
            agent="safety_gate",
            status="urgent",
            findings=[Finding("emergency_indicator", "Emergency warning sign reported.")],
            confidence="high",
            requires_human_review=True,
            recommendation="Urgent medical attention is recommended. Seek emergency care now.",
        )

    return AgentResult(
        agent="safety_gate",
        status="low",
        findings=[Finding("no_emergency_signals", "No immediate emergency indicator was reported.")],
        confidence="medium",
        requires_human_review=False,
        recommendation="Continue with routine screening and escalation guidance.",
    )
