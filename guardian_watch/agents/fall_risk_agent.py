from __future__ import annotations

from guardian_watch.core.schemas import AgentResult, Finding


def analyze_fall_risk(context_text: str) -> AgentResult:
    text = context_text.lower()
    findings: list[Finding] = []

    if any(keyword in text for keyword in ["near-fall", "near fall", "almost fell", "fell", "fall"]):
        findings.append(Finding("recent_falls_or_near_falls", "Recent fall or near-fall reported."))
    if any(keyword in text for keyword in ["unsteady", "wobbly", "holds furniture", "needs support", "difficulty walking"]):
        findings.append(Finding("mobility_instability", "Mobility or balance concern reported."))
    if any(keyword in text for keyword in ["night", "bathroom", "wakes up", "gets up at night"]):
        findings.append(Finding("nighttime_mobility", "Nighttime movement may increase fall risk."))
    if any(keyword in text for keyword in ["dizzy", "dizziness", "weak", "lightheaded"]):
        findings.append(Finding("dizziness_or_weakness", "Dizziness or weakness reported."))
    if any(keyword in text for keyword in ["rug", "clutter", "poor lighting", "loose carpet", "dim lighting"]):
        findings.append(Finding("home_hazard", "Home environment may contribute to fall risk."))

    if not findings:
        return AgentResult(
            agent="fall_risk",
            status="low",
            findings=[Finding("no_fall_signal", "No clear fall-risk indicators were reported.")],
            confidence="low",
            requires_human_review=False,
            recommendation="Continue routine monitoring.",
        )

    status = "monitor"
    if len(findings) >= 3:
        status = "review"
    if any(item.factor == "recent_falls_or_near_falls" and item.evidence for item in findings):
        status = "review"

    return AgentResult(
        agent="fall_risk",
        status=status,
        findings=findings,
        confidence="moderate",
        requires_human_review=True,
        recommendation="Discuss mobility and home-safety observations with a healthcare professional and review fall prevention measures.",
    )
