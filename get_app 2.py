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

st.image("https://upload.wikimedia.org/wikipedia/commons/3/3f/Green_leaf_icon.png", width=120)for c in criteria:
    choice = st.selectbox(c, ["Green", "Yellow", "Red"])
    total_score += score_map[choice]

st.subheader(f"Total Score: {total_score} / 28")

if total_score >= 22:
    st.success("Excellent greenness")
elif total_score >= 15:
    st.warning("Moderate greenness")
else:
    st.error("Low greenness")import pandas as pd

results = pd.DataFrame({
    "Parameter": parameters,
    "Score": scores
})

st.download_button(
    label="Download results as CSV",
    data=results.to_csv(index=False),
    file_name="green_extraction_results.csv",
    mime="text/csv"
)import plotly.graph_objects as go
import streamlit as st

categories = [
    "Solvent safety",
    "Energy consumption",
    "Waste generation",
    "Process safety",
    "Extraction efficiency"
]

scores = [2,1,2,1,2]   # punteggi GET

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=scores,
    theta=categories,
    fill='toself',
    name='Extraction method'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0,2]
        )),
    showlegend=False
)

st.subheader("Greenness profile")
st.plotly_chart(fig)fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=[1,0,1,0,2],
    theta=categories,
    fill='toself',
    name='Soxhlet'
))

fig.add_trace(go.Scatterpolar(
    r=[2,2,2,1,2],
    theta=categories,
    fill='toself',
    name='UAE'
))

fig.add_trace(go.Scatterpolar(
    r=[2,1,2,1,2],
    theta=categories,
    fill='toself',
    name='Maceration'
))

st.plotly_chart(fig)import plotly.express as px
import pandas as pd

data = pd.DataFrame({
    "Method":["Soxhlet","UAE","Maceration"],
    "Score":[8,11,9]
})

fig = px.bar(
    data,
    x="Method",
    y="Score",
    color="Method",
    title="Greenness score comparison"
)

st.plotly_chart(fig)import seaborn as sns
import matplotlib.pyplot as plt

matrix = [
    [1,0,1,0,2],
    [2,2,2,1,2],
    [2,1,2,1,2]
]

methods = ["Soxhlet","UAE","Maceration"]

fig, ax = plt.subplots()

sns.heatmap(matrix,
            annot=True,
            cmap="RdYlGn",
            xticklabels=categories,
            yticklabels=methods)

st.pyplot(fig)
