import streamlit as st
import pandas as pd
from datetime import datetime

# Simple UI Setup
st.set_page_config(page_title="Tournament Hand Logger", layout="centered")
st.title("♠️ Poker Hand Logger")

# --- Input Section ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        blinds = st.text_input("Blinds (e.g., 500/1000)", placeholder="500/1000")
        stack_bb = st.number_input("Your Stack (in BB)", min_value=1, value=40)
    
    with col2:
        position = st.selectbox("Your Position", 
            ["UTG", "UTG+1", "MP", "LJ", "HJ", "CO", "BTN", "SB", "BB"])
        hand = st.text_input("Your Hand", placeholder="AsKd")

# Action / Notes Section
action = st.text_area("Action Shorthand", placeholder="Hero opens 2.2x, BB defends. Flop J-7-2r...")

# --- Data Management ---
if st.button("Log Hand"):
    new_data = {
        "Timestamp": [datetime.now().strftime("%H:%M:%S")],
        "Blinds": [blinds],
        "Stack (BB)": [stack_bb],
        "Position": [position],
        "Hand": [hand],
        "Action": [action]
    }
    df = pd.DataFrame(new_data)
    
    # Save to a local CSV (Appends every time)
    df.to_csv("poker_hands.csv", mode='a', index=False, header=not st.io.isfile("poker_hands.csv"))
    st.success("Hand logged successfully!")

# --- Review Section ---
st.divider()
st.subheader("Today's Session")
try:
    history = pd.read_csv("poker_hands.csv")
    st.dataframe(history.tail(10)) # Shows last 10 hands
    
    # Export Button
    csv = history.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download All Hands (CSV)",
        data=csv,
        file_name="tournament_session.csv",
        mime="text/csv",
    )
except FileNotFoundError:
    st.info("No hands logged yet.")