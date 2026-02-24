import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Codeavour Referee System", layout="wide")

GOAL_POINTS = 10
BALL_HOLDING_PENALTY = 4
ILLEGAL_DEFENSE_PENALTY = 4
ROUGH_PLAY_PENALTY = 4
HAND_TOUCH_PENALTY = 12

st.title("🏆 CODEAVOUR ROBOSOCCER OMOTEC REFEREE SYSTEM")

# ==============================
# SESSION STORAGE
# ==============================
if "history" not in st.session_state:
    st.session_state.history = []

# ==============================
# TEAM INPUT
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
    st.subheader(teamA)
    goalsA = st.number_input("Goals (A)", 0)
    ballA = st.number_input("Ball Holding Fouls (A)", 0)
    defenseA = st.number_input("Illegal Defense Fouls (A)", 0)
    roughA = st.number_input("Rough Play Fouls (A)", 0)
    handA = st.number_input("Hand Touch Fouls (A)", 0)

with colB:
    st.subheader(teamB)
    goalsB = st.number_input("Goals (B)", 0)
    ballB = st.number_input("Ball Holding Fouls (B)", 0)
    defenseB = st.number_input("Illegal Defense Fouls (B)", 0)
    roughB = st.number_input("Rough Play Fouls (B)", 0)
    handB = st.number_input("Hand Touch Fouls (B)", 0)

st.divider()

# ==============================
# CALCULATE
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

    colR1, colR2 = st.columns(2)
    with colR1:
        st.metric(teamA, scoreA)
    with colR2:
        st.metric(teamB, scoreB)

    if scoreA > scoreB:
        winner = teamA
        st.success(f"🏆 {teamA} WINS!")
    elif scoreB > scoreA:
        winner = teamB
        st.success(f"🏆 {teamB} WINS!")
    else:
        winner = "DRAW"
        st.warning("⚽ DRAW - Penalty Shootout Required!")

    # Save to session
    match_data = {
        "Time": datetime.now(),
        "Team A": teamA,
        "Score A": scoreA,
        "Team B": teamB,
        "Score B": scoreB,
        "Winner": winner
    }

    st.session_state.history.append(match_data)

st.divider()

# ==============================
# MATCH HISTORY TABLE
# ==============================
if st.session_state.history:
    st.subheader("📊 Match History")

    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df)

    # Download button
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Match History (CSV)",
        data=csv,
        file_name="codeavour_match_history.csv",
        mime="text/csv"
    )
