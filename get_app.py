import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from graphviz import Digraph

st.set_page_config(page_title="Green Extraction Tree Evaluator", layout="wide")

st.title("🌿 Green Extraction Tree Evaluator")

st.markdown("""
Implementation inspired by the **Green Extraction Tree (GET)** framework.

Colors represent qualitative greenness:

🟢 Green = good  
🟡 Yellow = acceptable  
🔴 Red = problematic  

A numeric score is calculated **only as a synthetic indicator**, not as the primary GET evaluation.
""")

# ------------------------------------------------
# SOLVENT DATABASE (simplified green solvent guide)
# ------------------------------------------------

solvent_db = {

"Water":0,
"Ethanol":1,
"Ethyl acetate":1,
"Acetone":2,
"Methanol":3,
"Hexane":4,
"Dichloromethane":5,
"Chloroform":5

}

# ------------------------------------------------
# SCORING FUNCTIONS
# ------------------------------------------------

def color_score(value):

    if value == 2:
        return "green"
    elif value == 1:
        return "yellow"
    else:
        return "red"

def solvent_score(solvent):

    tox = solvent_db[solvent]

    if tox <=1:
        return 2
    elif tox <=3:
        return 1
    else:
        return 0

def volume_score(v):

    if v < 50:
        return 2
    elif v < 200:
        return 1
    else:
        return 0

def energy_score(e):

    if e < 0.5:
        return 2
    elif e < 2:
        return 1
    else:
        return 0

def time_score(t):

    if t < 30:
        return 2
    elif t < 120:
        return 1
    else:
        return 0

def yield_score(y):

    if y > 80:
        return 2
    elif y > 50:
        return 1
    else:
        return 0

def waste_score(w):

    if w < 5:
        return 2
    elif w < 20:
        return 1
    else:
        return 0

def throughput_score(t):

    if t > 20:
        return 2
    elif t > 5:
        return 1
    else:
        return 0

def hazard_score(h):

    if h == "Low":
        return 2
    elif h == "Medium":
        return 1
    else:
        return 0

def stability_score(s):

    if s == "Stable":
        return 2
    elif s == "Moderate":
        return 1
    else:
        return 0

def renewable_score(r):

    if r == "Yes":
        return 2
    elif r == "Partially":
        return 1
    else:
        return 0

def scalability_score(s):

    if s == "High":
        return 2
    elif s == "Moderate":
        return 1
    else:
        return 0

# ------------------------------------------------
# SESSION STATE
# ------------------------------------------------

if "methods" not in st.session_state:
    st.session_state.methods = []

# ------------------------------------------------
# INPUT PANEL
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
    ("Renewable raw material",renewable_score(renewable)),
    ("Sample stability",stability_score(sample_stability))
    ],

    "Solvents":[
    ("Solvent toxicity",solvent_score(solvent)),
    ("Solvent amount",volume_score(volume))
    ],

    "Energy":[
    ("Energy consumption",energy_score(energy)),
    ("Extraction time",time_score(time))
    ],

    "Waste":[
    ("Waste generation",waste_score(waste)),
    ("Byproduct formation",waste_score(waste))
    ],

    "Process risk":[
    ("Operational safety",hazard_score(hazard)),
    ("Health hazards",hazard
    
