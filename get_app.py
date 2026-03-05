import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Green Extraction Tree Lab", layout="wide")

st.title("Green Extraction Tree (GET) Evaluator")

st.markdown("""
Evaluation tool based on the **Green Extraction Tree (GET)** methodology.

Each criterion is scored:

Green = 2  
Yellow = 1  
Red = 0  

Maximum score = **28**
""")

criteria = [
"Renewable raw material",
"Sample stability",
"Solvent toxicity",
"Solvent amount",
"Energy consumption",
"Process time",
"Waste generation",
"Byproducts formation",
"Operational safety",
"Health hazards",
"Extraction efficiency",
"Extract stability",
"Industrial scalability",
"Throughput"
]

score_map = {"Green":2,"Yellow":1,"Red":0}

methods = st.multiselect(
"Extraction methods",
["Soxhlet","Ultrasound (UAE)","Maceration","Microwave (MAE)","Supercritical CO2"],
default=["Soxhlet"]
)

results={}
answers={}

for method in methods:

    st.header(method)

    choices=[]
    scores=[]

    for c in criteria:

        choice = st.radio(
            c,
            ["Green","Yellow","Red"],
            horizontal=True,
            key=f"{method}_{c}"
        )

        choices.append(choice)
        scores.append(score_map[choice])

    total=sum(scores)

    results[method]=scores
    answers[method]=choices

    st.subheader(f"GET Score: {total} / 28")

    if total>=22:
        st.success("Excellent greenness")
    elif total>=15:
        st.warning("Moderate greenness")
    else:
        st.error("Low greenness")

st.divider()

if len(results)>0:

    st.header("Radar profile")

    fig=go.Figure()

    for m in results:

        fig.add_trace(go.Scatterpolar(
            r=results[m],
            theta=criteria,
            fill="toself",
            name=m
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0,2],visible=True)),
        showlegend=True
    )

    st.plotly_chart(fig,use_container_width=True)

    st.header("Score comparison")

    scores_summary={m:sum(results[m]) for m in results}

    df=pd.DataFrame({
        "Method":list(scores_summary.keys()),
        "Score":list(scores_summary.values())
    })

    fig2=px.bar(df,x="Method",y="Score",color="Method")

    st.plotly_chart(fig2,use_container_width=True)

    st.header("Download results")

    rows=[]

    for m in results:

        for i,c in enumerate(criteria):

            rows.append({
                "Method":m,
                "Criterion":c,
                "Choice":answers[m][i],
                "Score":results[m][i]
            })

    df_export=pd.DataFrame(rows)

    st.download_button(
        "Download CSV",
        df_export.to_csv(index=False),
        file_name="GET_results.csv"
    )

st.divider()

st.markdown("""
### About GET

The **Green Extraction Tree** evaluates the sustainability of extraction
processes based on **14 criteria grouped into six categories**:

Sample  
Solvents & reagents  
Energy  
Waste & byproducts  
Process risk  
Extract quality
""")
