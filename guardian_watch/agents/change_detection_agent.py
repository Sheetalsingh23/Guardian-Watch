from __future__ import annotations

from guardian_watch.core.schemas import AgentResult, Finding


def analyze_change_pattern(context_text: str) -> AgentResult:
    text = context_text.lower()
    findings: list[Finding] = []

    if any(keyword in text for keyword in ["changed", "new", "recently", "over the last", "starts", "began"]):
        findings.append(Finding("recent_change_detected", "A recent change in routine or symptoms was reported."))
    if any(keyword in text for keyword in ["walking independently", "needs support", "holds furniture", "more unsteady", "changed walking"]):
        findings.append(Finding("mobility_change", "Observed mobility has changed compared with usual routine."))
    if any(keyword in text for keyword in ["wakes up several times", "nighttime bathroom", "urinate more at night", "sleep disruption"]):
        findings.append(Finding("sleep_pattern_change", "Nighttime bathroom trips or disrupted sleep were reported."))
    if any(keyword in text for keyword in ["dizzy", "dizziness", "weakness", "new symptom"]):
        findings.append(Finding("symptom_change", "A new or worsening symptom pattern was reported."))

    if not findings:
        return AgentResult(
            agent="change_detection",
            status="low",
            findings=[Finding("no_change_detected", "No meaningful routine change was identified.")],
            confidence="low",
            requires_human_review=False,
            recommendation="Continue routine observation and updates.",
        )

    status = "monitor"
    if len(findings) >= 2:
        status = "review"

    return AgentResult(
        agent="change_detection",
        status=status,
        findings=findings,
        confidence="moderate",
        requires_human_review=True,
        recommendation="New pattern detected. Consider documenting the changes and discussing them with a healthcare professional.",
    )
