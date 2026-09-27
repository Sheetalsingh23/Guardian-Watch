# Guardian Watch

Guardian Watch is a lightweight elder-care risk screener built as a multi-agent MVP. It gathers information about routine, medications, mobility, and recent changes, then runs a structured safety screen to flag potential fall or medication-related concerns without diagnosing a condition.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run guardian_watch/ui/streamlit_app.py
```

## Safety boundary

This system is intended for early screening and escalation support only. It does not diagnose illness or recommend changing medication without professional review.
