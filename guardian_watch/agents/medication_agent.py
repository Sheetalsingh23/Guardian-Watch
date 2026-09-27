from __future__ import annotations

import re

from guardian_watch.core.schemas import AgentResult, Finding


KNOWN_INTERACTIONS = {
    "dizziness": ["opioids", "sedatives", "antihistamines", "sleep medicines", "benzodiazepines"],
    "low_blood_pressure": ["antihypertensives", "diuretics", "beta blockers"],
    "sedation": ["sleep medicines", "benzodiazepines", "opioids", "antihistamines"],
}


def _parse_medications(text: str) -> list[str]:
    meds = re.findall(r"(?:new medication|medication|medicine|meds|prescription|started|takes)\s*(?:called\s*)?([A-Za-z][A-Za-z0-9\- ]{1,40})", text, flags=re.IGNORECASE)
    if meds:
        return [m.strip() for m in meds if m.strip()]
    return []


def analyze_medication_risk(context_text: str) -> AgentResult:
    text = context_text.lower()
    findings: list[Finding] = []

    if any(keyword in text for keyword in ["new medication", "new medicine", "started a new", "changed medication", "added medication"]):
        findings.append(Finding("new_medication", "A recent medication or dose change was reported."))

    if any(keyword in text for keyword in ["dizzy", "dizziness", "lightheaded", "weak"]):
        findings.append(Finding("dizziness_symptom", "Dizziness or lightheadedness was reported."))

    if any(keyword in text for keyword in ["blood pressure", "low blood pressure", "hypertension"]):
        findings.append(Finding("blood_pressure_issue", "Blood pressure concerns were reported."))

    if "sedation" in text or "sleepy" in text or "sleeping more" in text:
        findings.append(Finding("sedation", "Excessive sleepiness or sedation may be relevant."))

    if not findings:
        return AgentResult(
            agent="medication_risk",
            status="low",
            findings=[Finding("no_medication_concern", "No medication-related concern was clearly identified.")],
            confidence="low",
            requires_human_review=False,
            recommendation="Continue to maintain an updated medication list.",
        )

    status = "monitor"
    if "new medication" in text or len(findings) >= 2:
        status = "review"

    recommendation = (
        "Potential medication-related concern identified. This is not a medical diagnosis. "
        "Confirm with a pharmacist or clinician before changing medication."
    )

    return AgentResult(
        agent="medication_risk",
        status=status,
        findings=findings,
        confidence="moderate",
        requires_human_review=True,
        recommendation=recommendation,
    )
