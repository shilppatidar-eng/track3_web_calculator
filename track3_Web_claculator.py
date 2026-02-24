import streamlit as st
import pandas as pd
from datetime import datetime

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="Codeavour Referee System", layout="wide")

GOAL_POINTS = 10
BALL_HOLDING_PENALTY = 4
ILLEGAL_DEFENSE_PENALTY = 4
ROUGH_PLAY_PENALTY = 4
HAND_TOUCH_PENALTY = 12

MATCH_TIME = 300

# ==============================
# TITLE
# ==============================
st.title("🏆 CODEAVOUR ROBOSOCCER OFFICIAL REFEREE SYSTEM")

# ==============================
# TEAM NAMES
# ==============================
col1, col2 = st.columns(2)
with col1:
    teamA = st.text_input("Team A Name", "TEAM A")
with col2:
    teamB = st.text_input("Team B Name", "TEAM B")

st.divider()

# ==============================
# SCORE INPUT
# ==============================
colA, colB = st.columns(2)

with colA:
    st.subheader(f"{teamA} Controls")
    goalsA = st.number_input("Goals (A)", 0)
    ballA = st.number_input("Ball Holding Fouls (A)", 0)
    defenseA = st.number_input("Illegal Defense Fouls (A)", 0)
    roughA = st.number_input("Rough Play Fouls (A)", 0)
    handA = st.number_input("Hand Touch Fouls (A)", 0)

with colB:
    st.subheader(f"{teamB} Controls")
    goalsB = st.number_input("Goals (B)", 0)
    ballB = st.number_input("Ball Holding Fouls (B)", 0)
    defenseB = st.number_input("Illegal Defense Fouls (B)", 0)
    roughB = st.number_input("Rough Play Fouls (B)", 0)
    handB = st.number_input("Hand Touch Fouls (B)", 0)

st.divider()

# ==============================
# CALCULATION
# ==============================

if st.button("Calculate Score"):

    foulA = (ballA * BALL_HOLDING_PENALTY) + \
            (defenseA * ILLEGAL_DEFENSE_PENALTY) + \
            (roughA * ROUGH_PLAY_PENALTY) + \
            (handA * HAND_TOUCH_PENALTY)

    foulB = (ballB * BALL_HOLDING_PENALTY) + \
            (defenseB * ILLEGAL_DEFENSE_PENALTY) + \
            (roughB * ROUGH_PLAY_PENALTY) + \
            (handB * HAND_TOUCH_PENALTY)

    scoreA = (goalsA * GOAL_POINTS) - foulA
    scoreB = (goalsB * GOAL_POINTS) - foulB

    st.success("Match Result")

    colR1, colR2 = st.columns(2)
    with colR1:
        st.metric(teamA, scoreA)
    with colR2:
        st.metric(teamB, scoreB)

    if scoreA > scoreB:
        st.success(f"🏆 {teamA} WINS!")
        winner = teamA
    elif scoreB > scoreA:
        st.success(f"🏆 {teamB} WINS!")
        winner = teamB
    else:
        st.warning("⚽ DRAW - Penalty Shootout Required!")
        winner = "DRAW"

    # Save history
    data = {
        "Time": datetime.now(),
        "Team A": teamA,
        "Score A": scoreA,
        "Team B": teamB,
        "Score B": scoreB,
        "Winner": winner
    }

    df = pd.DataFrame([data])
    df.to_csv("match_history.csv", mode="a", header=False, index=False)

    st.info("Match saved to history.")