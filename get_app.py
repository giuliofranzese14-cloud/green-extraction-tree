import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Green Extraction Tree", layout="wide")

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

answers = []
scores = []

st.header("Evaluation")

for c in criteria:
    choice = st.radio(c, ["Green", "Yellow", "Red"], horizontal=True)
    answers.append(choice)
    scores.append(score_map[choice])

total_score = sum(scores)

st.subheader(f"Total Score: {total_score} / 28")

if total_score >= 22:
    st.success("Excellent greenness")
elif total_score >= 15:
    st.warning("Moderate greenness")
else:
    st.error("Low greenness")

# dataframe risultati
results = pd.DataFrame({
    "Parameter": criteria,
    "Choice": answers,
    "Score": scores
})

st.download_button(
    label="Download results as CSV",
    data=results.to_csv(index=False),
    file_name="green_extraction_results.csv",
    mime="text/csv"
)

st.header("Greenness profile")

# radar chart
fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=scores,
    theta=criteria,
    fill='toself',
    name='Current extraction'
))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0,2])),
    showlegend=False
)

st.plotly_chart(fig)

st.header("Method comparison")

data = pd.DataFrame({
    "Method": ["Soxhlet","UAE","Maceration"],
    "Score": [8,11,9]
})

fig_bar = px.bar(
    data,
    x="Method",
    y="Score",
    color="Method",
    title="Greenness score comparison"
)

st.plotly_chart(fig_bar)

# heatmap
matrix = [
    [1,0,1,0,2],
    [2,2,2,1,2],
    [2,1,2,1,2]
]

methods = ["Soxhlet","UAE","Maceration"]
categories = [
    "Solvent safety",
    "Energy consumption",
    "Waste generation",
    "Process safety",
    "Extraction efficiency"
]

fig_heat, ax = plt.subplots()

sns.heatmap(
    matrix,
    annot=True,
    cmap="RdYlGn",
    xticklabels=categories,
    yticklabels=methods
)

st.pyplot(fig_heat)
