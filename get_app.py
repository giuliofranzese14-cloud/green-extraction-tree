import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Green Extraction Tree Lab", layout="wide")

st.title("Green Extraction Tree (GET) Evaluator")

st.markdown("""
Interactive evaluation tool for assessing the **greenness of extraction methods**
according to the **Green Extraction Tree (GET)** framework.

Each criterion receives:

Green = 2  
Yellow = 1  
Red = 0  

Maximum GET score = **28**.
""")

criteria_tree = {
"Sample": [
"Renewable raw material",
"Sample stability"
],

"Solvents & Reagents": [
"Solvent toxicity",
"Solvent amount"
],

"Energy": [
"Energy consumption",
"Process time"
],

"Waste & Byproducts": [
"Waste generation",
"Byproducts formation"
],

"Process Risk": [
"Operational safety",
"Health hazards"
],

"Extract Quality": [
"Extraction efficiency",
"Extract stability",
"Industrial scalability",
"Throughput"
]
}

score_map = {"Green":2,"Yellow":1,"Red":0}

methods = st.multiselect(
"Select extraction methods to evaluate",
["Soxhlet","Ultrasound (UAE)","Maceration","Microwave (MAE)","Supercritical CO2"],
default=["Soxhlet"]
)

results = {}
answers_store = {}

for method in methods:

    st.header(method)

    answers=[]
    scores=[]

    for branch in criteria_tree:

        st.subheader(branch)

        for criterion in criteria_tree[branch]:

            choice = st.radio(
                criterion,
                ["Green","Yellow","Red"],
                horizontal=True,
                key=f"{method}_{criterion}"
            )

            answers.append(choice)
            scores.append(score_map[choice])

    total_score=sum(scores)

    results[method]=scores
    answers_store[method]=answers

    st.subheader(f"Total GET Score: {total_score} / 28")

    if total_score>=22:
        st.success("Excellent greenness")
    elif total_score>=15:
        st.warning("Moderate greenness")
    else:
        st.error("Low greenness")

st.divider()

if len(results)>0:

    st.header("Greenness Radar Profile")

    all_criteria=[c for branch in criteria_tree.values() for c in branch]

    fig=go.Figure()

    for method in results:

        fig.add_trace(go.Scatterpolar(
            r=results[method],
            theta=all_criteria,
            fill="toself",
            name=method
        ))

    fig.update_layout(
    polar=dict(radialaxis=dict(range=[0,2],visible=True)),
    showlegend=True
    )

    st.plotly_chart(fig,use_container_width=True)

    st.divider()

    st.header("Greenness Score Comparison")

    score_summary={
    m:sum(results[m]) for m in results
    }

    df_scores=pd.DataFrame({
    "Method":list(score_summary.keys()),
    "Score":list(score_summary.values())
    })

    fig_bar=px.bar(
    df_scores,
    x="Method",
    y="Score",
    color="Method",
    title="GET score comparison"
    )

    st.plotly_chart(fig_bar,use_container_width=True)

    st.divider()

    st.header("Criterion Heatmap")

    matrix=list(results.values())

    fig_heat,ax=plt.subplots(figsize=(12,4))

    sns.heatmap(
    matrix,
    annot=True,
    cmap="RdYlGn",
    xticklabels=all_criteria,
    yticklabels=list(results.keys())
    )

    st.pyplot(fig_heat)

    st.divider()

    st.header("Download Results")

    export_rows=[]

    for method in results:

        for i,c in enumerate(all_criteria):

            export_rows.append({
            "Method":method,
            "Criterion":c,
            "Choice":answers_store[method][i],
            "Score":results[method][i]
            })

    df_export=pd.DataFrame(export_rows)

    st.download_button(
    "Download results as CSV",
    df_export.to_csv(index=False),
    file_name="green_extraction_results.csv"
    )

st.divider()

st.markdown("""
### About GET

The **Green Extraction Tree (GET)** evaluates the sustainability of natural product extraction processes through **six main branches**:

- Sample
- Solvents & reagents
- Energy
- Waste & byproducts
- Process risk
- Extract quality

Each branch includes specific criteria that together define the environmental and operational greenness of the process.
""")
