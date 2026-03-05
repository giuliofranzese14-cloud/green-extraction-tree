import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Green Extraction Tree 3.0", layout="wide")

st.title("🌿 Green Extraction Tree Evaluator 3.0")

st.markdown("""
Advanced evaluation tool based on the **Green Extraction Tree (GET)** framework.

Each criterion is automatically classified:

Green = 2  
Yellow = 1  
Red = 0  

Maximum score = **28**
""")

st.sidebar.header("Extraction parameters")

method_name = st.sidebar.text_input("Method name", "Extraction Method")

solvent_type = st.sidebar.selectbox(
    "Solvent type",
    ["Water","Ethanol","Methanol","Hexane","Dichloromethane","Chloroform"]
)

solvent_volume = st.sidebar.number_input("Solvent volume (mL)", 0.0, 1000.0, 50.0)

energy = st.sidebar.number_input("Energy consumption (kWh)", 0.0, 10.0, 0.5)

time = st.sidebar.number_input("Extraction time (minutes)", 1, 1000, 60)

yield_percent = st.sidebar.slider("Extraction yield (%)", 0, 100, 50)

waste = st.sidebar.number_input("Waste generated (g)", 0.0, 500.0, 10.0)

throughput = st.sidebar.number_input("Samples per hour", 1, 100, 5)

hazard = st.sidebar.selectbox(
    "Health hazard level",
    ["Low","Medium","High"]
)

renewable_sample = st.sidebar.selectbox(
    "Renewable raw material?",
    ["Yes","Partially","No"]
)

sample_stability = st.sidebar.selectbox(
    "Sample stability",
    ["Stable","Moderate","Unstable"]
)

industrial_scalability = st.sidebar.selectbox(
    "Industrial scalability",
    ["High","Moderate","Low"]
)

extract_stability = st.sidebar.selectbox(
    "Extract stability",
    ["Stable","Moderate","Unstable"]
)

# ---------------------------
# Scoring functions
# ---------------------------

def score_solvent_type(solvent):
    green = ["Water","Ethanol"]
    yellow = ["Methanol"]
    if solvent in green:
        return 2
    elif solvent in yellow:
        return 1
    else:
        return 0

def score_volume(v):
    if v < 50:
        return 2
    elif v < 200:
        return 1
    else:
        return 0

def score_energy(e):
    if e < 0.5:
        return 2
    elif e < 2:
        return 1
    else:
        return 0

def score_time(t):
    if t < 30:
        return 2
    elif t < 120:
        return 1
    else:
        return 0

def score_yield(y):
    if y > 80:
        return 2
    elif y > 50:
        return 1
    else:
        return 0

def score_waste(w):
    if w < 5:
        return 2
    elif w < 20:
        return 1
    else:
        return 0

def score_throughput(t):
    if t > 20:
        return 2
    elif t > 5:
        return 1
    else:
        return 0

def score_hazard(h):
    if h == "Low":
        return 2
    elif h == "Medium":
        return 1
    else:
        return 0

def score_renewable(r):
    if r == "Yes":
        return 2
    elif r == "Partially":
        return 1
    else:
        return 0

def score_stability(s):
    if s == "Stable":
        return 2
    elif s == "Moderate":
        return 1
    else:
        return 0

def score_scalability(s):
    if s == "High":
        return 2
    elif s == "Moderate":
        return 1
    else:
        return 0

# ---------------------------
# Criteria tree
# ---------------------------

criteria = {
"Sample":[
("Renewable raw material",score_renewable(renewable_sample)),
("Sample stability",score_stability(sample_stability))
],

"Solvents":[
("Solvent toxicity",score_solvent_type(solvent_type)),
("Solvent amount",score_volume(solvent_volume))
],

"Energy":[
("Energy consumption",score_energy(energy)),
("Process time",score_time(time))
],

"Waste":[
("Waste generation",score_waste(waste)),
("Byproducts formation",score_waste(waste))
],

"Process risk":[
("Operational safety",score_hazard(hazard)),
("Health hazards",score_hazard(hazard))
],

"Extract quality":[
("Extraction efficiency",score_yield(yield_percent)),
("Extract stability",score_stability(extract_stability)),
("Industrial scalability",score_scalability(industrial_scalability)),
("Throughput",score_throughput(throughput))
]
}

# ---------------------------
# Calculate score
# ---------------------------

scores=[]
labels=[]

for branch in criteria:

    for item in criteria[branch]:

        labels.append(item[0])
        scores.append(item[1])

total_score=sum(scores)

st.header("GET Score")

st.metric("Total score", f"{total_score} / 28")

if total_score >=22:
    st.success("Excellent greenness")
elif total_score >=15:
    st.warning("Moderate greenness")
else:
    st.error("Low greenness")

# ---------------------------
# Tree visualization
# ---------------------------

st.header("GET Tree")

for branch in criteria:

    st.subheader(branch)

    for name,value in criteria[branch]:

        if value == 2:
            color="🟢"
        elif value ==1:
            color="🟡"
        else:
            color="🔴"

        st.write(color, name)

# ---------------------------
# Radar chart
# ---------------------------

st.header("Greenness radar")

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=scores,
    theta=labels,
    fill="toself",
    name=method_name
))

fig.update_layout(
polar=dict(radialaxis=dict(range=[0,2])),
showlegend=False
)

st.plotly_chart(fig,use_container_width=True)

# ---------------------------
# Score breakdown
# ---------------------------

st.header("Score breakdown")

df=pd.DataFrame({
"Criterion":labels,
"Score":scores
})

st.dataframe(df)

# ---------------------------
# Bar chart
# ---------------------------

fig2=px.bar(df,x="Criterion",y="Score",color="Score")

st.plotly_chart(fig2,use_container_width=True)

# ---------------------------
# Export results
# ---------------------------

st.header("Export results")

csv=df.to_csv(index=False)

st.download_button(
"Download CSV",
csv,
"GET_results.csv",
"text/csv"
)

# ---------------------------
# Method comparison placeholder
# ---------------------------

st.header("Future comparison module")

st.info("Future versions will allow comparison between multiple extraction methods.")
