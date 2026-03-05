import streamlit as st

st.title("Green Extraction Tree (GET)")

criteria = [
    "Promote renewable materials",
    "Ensure sample stability",
    "Minimize sample amount",
    "Use safer solvents",
    "Minimize solvent amount",
    "Minimize preparation steps",
    "Minimize energy consumption",
    "Maximize throughput",
    "Maximize extraction efficiency",
    "Minimize waste generation",
    "Reduce health hazards",
    "Reduce operational risks",
    "Greener analytical detection",
    "Industrial production prospects"
]

score_map = {"Green": 2, "Yellow": 1, "Red": 0}

total_score = 0

for c in criteria:
    choice = st.selectbox(c, ["Green", "Yellow", "Red"])
    total_score += score_map[choice]

st.subheader(f"Total Score: {total_score} / 28")

if total_score >= 22:
    st.success("Excellent greenness")
elif total_score >= 15:
    st.warning("Moderate greenness")
else:
    st.error("Low greenness")