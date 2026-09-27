from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from guardian_watch.core.orchestrator import run_screening
from guardian_watch.core.schemas import ElderContext


st.set_page_config(page_title="Guardian Watch", page_icon="🛡️", layout="wide")

st.markdown(
    """
    <style>
    .main { background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%); }
    h1 { color: #0f172a; }
    .stApp { max-width: 1400px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Guardian Watch: Elder Care Risk Screener")
st.caption("Screen for patterns, not diagnoses — explain, escalate, and recommend human review.")

col1, col2 = st.columns([1.3, 0.7])

with col1:
    with st.form("guardian_watch_form"):
        elder_name = st.text_input("Elder's name", value="Mother")
        age = st.number_input("Age", min_value=50, max_value=120, value=76)
        daily_routine = st.text_area(
            "Daily routine",
            value="Normally walks independently. Uses the bathroom during the night and takes short walks around the home.",
        )
        medications = st.text_area(
            "Medications and recent changes",
            value="Started a new medicine last week for sleep. Also takes a blood pressure medicine each morning.",
        )
        recent_changes = st.text_area(
            "Recent changes",
            value="Over the last two weeks, walking has become less steady and she holds furniture while moving around.",
        )
        mobility = st.text_area(
            "Mobility and walking habits",
            value="Holds furniture while walking. Went from independently walking to needing support recently.",
        )
        home_factors = st.text_area(
            "Home/environment factors",
            value="Loose rug in hallway, dim lighting near bedroom, nighttime trips to bathroom.",
        )
        behavioral_changes = st.text_area(
            "Behavioral changes",
            value="Reports dizziness and near-falls in the past few days.",
        )
        recent_falls = st.text_area(
            "Recent falls or near-falls",
            value="Yesterday felt dizzy and almost fell. Two near-falls this week.",
        )
        baseline_routine = st.text_area(
            "Usual baseline routine",
            value="She usually walked independently and slept normally without dizziness.",
        )

        submitted = st.form_submit_button("Run Guardian Watch", use_container_width=True)

with col2:
    st.markdown("### Safety note")
    st.info(
        "This is a screening tool designed to identify patterns for discussion with a clinician or pharmacist. It is not a diagnosis and it does not recommend medication changes on its own."
    )
    st.markdown("### Demo scenario")
    st.code(
        "My 76-year-old mother normally walks independently. Over the last two weeks she has started holding furniture while walking. She wakes up several times at night to use the bathroom. She started a new medicine last week. Yesterday she felt dizzy and almost fell.",
        language="text",
    )

if submitted:
    context = ElderContext(
        elder_name=elder_name,
        age=age,
        daily_routine=daily_routine,
        medications=medications,
        recent_changes=recent_changes,
        mobility=mobility,
        home_factors=home_factors,
        behavioral_changes=behavioral_changes,
        recent_falls=recent_falls,
        baseline_routine=baseline_routine,
    )

    result = run_screening(context)

    st.subheader("Risk Screen")
    status = result["status"]
    if status == "urgent":
        st.error(f"{result['status_label']} — {result['summary']}")
    elif status == "review":
        st.warning(f"{result['status_label']} — {result['summary']}")
    elif status == "monitor":
        st.info(f"{result['status_label']} — {result['summary']}")
    else:
        st.success(f"{result['status_label']} — {result['summary']}")

    st.markdown("### What we noticed")
    st.write(result["reason"])
    st.write(result["explanation"])
    st.write("Recommended next step: " + result["recommendation"])

    st.markdown("### Evidence trail")
    for step in result["evidence_trail"]:
        st.write(f"- {step}")

    st.markdown("### Agent outputs")
    for agent in result["agents"]:
        with st.expander(agent["agent"].replace("_", " ").title()):
            st.json(agent)
