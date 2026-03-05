import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from graphviz import Digraph

st.set_page_config(page_title="Green Extraction Tree 6.0", layout="wide")

st.title("🌿 Green Extraction Tree Evaluator 6.0")

st.markdown("""
Interactive platform implementing the **Green Extraction Tree (GET)** methodology.

Green = 2  
Yellow = 1  
Red = 0  

Maximum score = **28**
""")

# ------------------------------------------------
# SOLVENT DATABASE
# ------------------------------------------------

solvent_db = {

"Water":{"toxicity":0},
"Ethanol":{"toxicity":1},
"Methanol":{"toxicity":2},
"Acetone":{"toxicity":2},
"Hexane":{"toxicity":3},
"Dichloromethane":{"toxicity":4},
"Chloroform":{"toxicity":5}

}

# ------------------------------------------------
# SCORING FUNCTIONS
# ------------------------------------------------

def score_solvent(solvent):

    tox = solvent_db[solvent]["toxicity"]

    if tox <=1:
        return 2
    elif tox <=3:
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


def score_stability(s):

    if s == "Stable":
        return 2
    elif s == "Moderate":
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


def score_scalability(s):

    if s == "High":
        return 2
    elif s == "Moderate":
        return 1
    else:
        return 0


# ------------------------------------------------
# SESSION STORAGE
# ------------------------------------------------

if "methods" not in st.session_state:
    st.session_state.methods = []


# ------------------------------------------------
# SIDEBAR INPUT
# ------------------------------------------------

st.sidebar.header("Extraction parameters")

method_name = st.sidebar.text_input("Method name")

solvent = st.sidebar.selectbox("Solvent", list(solvent_db.keys()))

volume = st.sidebar.number_input("Solvent volume (mL)",0.0,1000.0,50.0)

energy = st.sidebar.number_input("Energy consumption (kWh)",0.0,10.0,0.5)

time = st.sidebar.number_input("Extraction time (min)",1,1000,60)

yield_percent = st.sidebar.slider("Yield (%)",0,100,50)

waste = st.sidebar.number_input("Waste (g)",0.0,500.0,10.0)

throughput = st.sidebar.number_input("Samples/hour",1,100,5)

hazard = st.sidebar.selectbox("Hazard level",["Low","Medium","High"])

renewable = st.sidebar.selectbox("Renewable raw material",["Yes","Partially","No"])

sample_stability = st.sidebar.selectbox("Sample stability",["Stable","Moderate","Unstable"])

extract_stability = st.sidebar.selectbox("Extract stability",["Stable","Moderate","Unstable"])

scalability = st.sidebar.selectbox("Industrial scalability",["High","Moderate","Low"])


# ------------------------------------------------
# GET CALCULATION
# ------------------------------------------------

def compute_get():

    tree = {

"Sample":[
("Renewable raw material",score_renewable(renewable)),
("Sample stability",score_stability(sample_stability))
],

"Solvents":[
("Solvent toxicity",score_solvent(solvent)),
("Solvent amount",score_volume(volume))
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
("Industrial scalability",score_scalability(scalability)),
("Throughput",score_throughput(throughput))
]

}

    labels=[]
    scores=[]

    for branch in tree:

        for item in tree[branch]:

            labels.append(item[0])
            scores.append(item[1])

    total=sum(scores)

    return tree,labels,scores,total


# ------------------------------------------------
# ADD METHOD
# ------------------------------------------------

if st.sidebar.button("Add method"):

    tree,labels,scores,total = compute_get()

    st.session_state.methods.append({

"name":method_name,
"tree":tree,
"labels":labels,
"scores":scores,
"total":total

})


# ------------------------------------------------
# DISPLAY METHODS
# ------------------------------------------------

for method in st.session_state.methods:

    st.header(method["name"])

    st.metric("GET Score",f'{method["total"]}/28')

    st.subheader("GET Tree")

    dot = Digraph()

    dot.node("GET","GET")

    for branch in method["tree"]:

        dot.node(branch,branch)

        dot.edge("GET",branch)

        for name,value in method["tree"][branch]:

            node = name

            if value==2:
                color="green"
            elif value==1:
                color="yellow"
            else:
                color="red"

            dot.node(node,style="filled",fillcolor=color)

            dot.edge(branch,node)

    st.graphviz_chart(dot)


# ------------------------------------------------
# COMPARISON
# ------------------------------------------------

if len(st.session_state.methods) > 1:

    st.header("Radar comparison")

    radar = go.Figure()

    for method in st.session_state.methods:

        radar.add_trace(go.Scatterpolar(

        r=method["scores"],
        theta=method["labels"],
        fill="toself",
        name=method["name"]

        ))

    radar.update_layout(polar=dict(radialaxis=dict(range=[0,2])))

    st.plotly_chart(radar,use_container_width=True)


# ------------------------------------------------
# RANKING
# ------------------------------------------------

if len(st.session_state.methods) > 1:

    ranking = sorted(

    st.session_state.methods,
    key=lambda x: x["total"],
    reverse=True

    )

    st.header("Greenest method ranking")

    rank_df = pd.DataFrame({

    "Method":[m["name"] for m in ranking],
    "GET score":[m["total"] for m in ranking]

    })

    st.dataframe(rank_df)

    fig = px.bar(rank_df,x="Method",y="GET score",color="Method")

    st.plotly_chart(fig,use_container_width=True)


# ------------------------------------------------
# HEATMAP
# ------------------------------------------------

if len(st.session_state.methods) > 1:

    st.header("Score heatmap")

    matrix=[m["scores"] for m in st.session_state.methods]

    labels = st.session_state.methods[0]["labels"]

    names=[m["name"] for m in st.session_state.methods]

    fig,ax=plt.subplots()

    sns.heatmap(matrix,
                annot=True,
                cmap="RdYlGn",
                xticklabels=labels,
                yticklabels=names)

    st.pyplot(fig)


# ------------------------------------------------
# EXPORT
# ------------------------------------------------

if len(st.session_state.methods) > 0:

    rows=[]

    for m in st.session_state.methods:

        for i,c in enumerate(m["labels"]):

            rows.append({

            "Method":m["name"],
            "Criterion":c,
            "Score":m["scores"][i]

            })

    df=pd.DataFrame(rows)

    csv=df.to_csv(index=False)

    st.download_button(

    "Download results CSV",
    csv,
    "GET_results.csv",
    "text/csv"

    )
   import graphviz

st.header("Green Extraction Tree")

def draw_get_tree(tree):

    dot = graphviz.Digraph()

    dot.attr(rankdir="TB")

    dot.node("GET","Green Extraction Tree",shape="box")

    for branch in tree:

        dot.node(branch,branch,shape="ellipse")

        dot.edge("GET",branch)

        for name,value in tree[branch]:

            node_id = f"{branch}_{name}"

            if value == 2:
                color = "green"
            elif value == 1:
                color = "yellow"
            else:
                color = "red"

            dot.node(
                node_id,
                name,
                style="filled",
                fillcolor=color
            )

            dot.edge(branch,node_id)

    return dot


# disegna l'albero per ogni metodo salvato
for method in st.session_state.methods:

    st.subheader(f"GET Tree — {method['name']}")

    tree = method["tree"]

    dot = draw_get_tree(tree)

    st.graphviz_chart(dot)
