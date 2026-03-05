import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Green Extraction Evaluator", layout="wide")

st.title("Green Extraction Evaluator")

st.markdown("""
Interactive platform for evaluating the **greenness of extraction methods**
based on the **Green Extraction Tree (GET)** framework.
""")

st.sidebar.header("Extraction parameters")

method = st.sidebar.selectbox(
"Extraction method",
["Soxhlet","Ultrasound (UAE)","Maceration"]
)

solvent = st.sidebar.selectbox(
"Solvent",
["Water","Ethanol","Ethyl acetate","Hexane"]
)

solvent_volume = st.sidebar.slider(
"Solvent volume (mL)",
10,500,50
)

energy = st.sidebar.slider(
"Energy consumption (kWh)",
0.1,5.0,1.0
)

yield_value = st.sidebar.slider(
"Extraction yield (%)",
10,100,80
)

time = st.sidebar.slider(
"Extraction time (min)",
10,600,120
)

score = 0

if solvent in ["Water","Ethanol"]:
    solvent_score = 2
else:
    solvent_score = 0

score += solvent_score

if solvent_volume < 100:
    score += 2
elif solvent_volume < 200:
    score += 1

if energy < 1:
    score += 2
elif energy < 2:
    score += 1

if yield_value > 80:
    score += 2
elif yield_value > 60:
    score += 1

if time < 120:
    score += 2
elif time < 240:
    score += 1

st.header("Greenness score")

st.metric("GET score",score)

if score >= 8:
    st.success("High greenness")
elif score >=5:
    st.warning("Moderate greenness")
else:
    st.error("Low greenness")

st.header("Greenness profile")

categories = [
"Solvent safety",
"Solvent amount",
"Energy",
"Extraction time",
"Yield"
]

values = [
solvent_score,
2 if solvent_volume <100 else 1,
2 if energy<1 else 1,
2 if time<120 else 1,
2 if yield_value>80 else 1
]

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
r=values,
theta=categories,
fill="toself",
name=method
))

fig.update_layout(
polar=dict(radialaxis=dict(range=[0,2])),
showlegend=False
)

st.plotly_chart(fig)

st.header("Comparison example")

data = pd.DataFrame({
"Method":["Soxhlet","UAE","Maceration"],
"Score":[4,9,7]
})

fig2 = px.bar(
data,
x="Method",
y="Score",
color="Method",
title="Greenness comparison"
)

st.plotly_chart(fig2)
