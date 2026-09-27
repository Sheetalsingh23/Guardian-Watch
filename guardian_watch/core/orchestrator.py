from __future__ import annotations

from guardian_watch.agents.change_detection_agent import analyze_change_pattern
from guardian_watch.agents.cross_check_agent import cross_check
from guardian_watch.agents.escalation_agent import create_escalation
from guardian_watch.agents.fall_risk_agent import analyze_fall_risk
from guardian_watch.agents.medication_agent import analyze_medication_risk
from guardian_watch.agents.safety_agent import evaluate_safety
from guardian_watch.core.risk_engine import determine_final_status, describe_risk_summary
from guardian_watch.core.schemas import ElderContext


def run_screening(context: ElderContext) -> dict:
    text = context.as_text()

    safety = evaluate_safety(text)
    if safety.status == "urgent":
        return {
            "status": "urgent",
            "status_label": "URGENT",
            "summary": describe_risk_summary("urgent", 1),
            "agents": [safety.to_dict()],
            "explanation": "Emergency indicators were reported. This screening is paused in favor of immediate emergency guidance.",
            "recommendation": "Seek emergency medical attention immediately.",
            "evidence_trail": ["User input", "Safety Gate Agent", "Emergency escalation"],
        }

    fall_agent = analyze_fall_risk(text)
    medication_agent = analyze_medication_risk(text)
    change_agent = analyze_change_pattern(text)
    cross_agent = cross_check([fall_agent, medication_agent, change_agent])

    results = [safety, fall_agent, medication_agent, change_agent, cross_agent]
    final_status, reason = determine_final_status(results)
    findings_count = sum(len(result.findings) for result in results if result.status != "low")
    escalation = create_escalation(final_status, findings_count)

    explanation = (
        "The reported pattern includes mobility changes, recent medication or routine changes, and possible dizziness or near-fall symptoms. "
        "This pattern may warrant professional review but is not a diagnosis."
    )

    return {
        "status": final_status,
        "status_label": final_status.upper() if final_status != "low" else "LOW",
        "summary": describe_risk_summary(final_status, findings_count),
        "reason": reason,
        "agents": [
            safety.to_dict(),
            fall_agent.to_dict(),
            medication_agent.to_dict(),
            change_agent.to_dict(),
            cross_agent.to_dict(),
            escalation.to_dict(),
        ],
        "explanation": explanation,
        "recommendation": "Discuss these observations and the medication list with the elder's healthcare professional or pharmacist before making any medication changes.",
        "evidence_trail": [
            "User input",
            "Medication Agent",
            "Fall Agent",
            "Change Agent",
            "Cross-check Agent",
            "Safety Agent",
            "Escalation Agent",
        ],
    }
