import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Green Extraction Tree", layout="wide")

st.title("Green Extraction Tree (GET) – Extraction Sustainability Evaluator")

st.markdown("""
Interactive tool to evaluate the **greenness of extraction methods** according to the
Green Extraction Tree framework.

Compare different extraction techniques such as:

- Soxhlet extraction
- Ultrasound-assisted extraction (UAE)
- Maceration
""")

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

score_map = {"Green":2,"Yellow":1,"Red":0}

methods = st.multiselect(
"Select extraction methods to evaluate",
["Soxhlet","Ultrasound (UAE)","Maceration"],
default=["Soxhlet"]
)

results = {}

for method in methods:

    st.header(method)

    answers=[]
    scores=[]

    for c in criteria:
        choice = st.radio(
            c,
            ["Green","Yellow","Red"],
            key=method+c,
            horizontal=True
        )

        answers.append(choice)
        scores.append(score_map[choice])

    total_score=sum(scores)

    results[method]=scores

    st.subheader(f"Total Score: {total_score} / 28")

    if total_score>=22:
        st.success("Excellent greenness")
    elif total_score>=15:
        st.warning("Moderate greenness")
    else:
        st.error("Low greenness")

st.header("Radar comparison")

fig=go.Figure()

for method in results:

    fig.add_trace(go.Scatterpolar(
        r=results[method],
        theta=criteria,
        fill="toself",
        name=method
    ))

fig.update_layout(
polar=dict(radialaxis=dict(range=[0,2],visible=True)),
showlegend=True
)

st.plotly_chart(fig,use_container_width=True)

st.header("Score comparison")

scores_summary={
method:sum(results[method]) for method in results
}

df_scores=pd.DataFrame({
"Method":list(scores_summary.keys()),
"Score":list(scores_summary.values())
})

fig_bar=px.bar(
df_scores,
x="Method",
y="Score",
color="Method",
title="Greenness score comparison"
)

st.plotly_chart(fig_bar,use_container_width=True)

st.header("Heatmap comparison")

matrix=list(results.values())

if len(matrix)>0:

    fig_heat,ax=plt.subplots()

    sns.heatmap(
        matrix,
        annot=True,
        cmap="RdYlGn",
        xticklabels=criteria,
        yticklabels=list(results.keys())
    )

    st.pyplot(fig_heat)

st.header("Download results")

export_data=[]

for method in results:

    for i,c in enumerate(criteria):

        export_data.append({
            "Method":method,
            "Criterion":c,
            "Score":results[method][i]
        })

df_export=pd.DataFrame(export_data)

st.download_button(
"Download results CSV",
df_export.to_csv(index=False),
file_name="green_extraction_results.csv"
)

st.markdown("---")
st.markdown("Green Extraction Tree evaluation tool")

   
