import streamlit as st

st.title("🥁 Do you LOVE or HATE drumming at sports games?")
st.write("Vote first — see results after you unlock them with your email.")

if st.button("❤️ LOVE IT"):
    st.session_state.vote = "love"
    st.session_state.step = "email_gate"
    st.rerun()

if st.button("💢 HATE IT"):
    st.session_state.vote = "hate"
    st.session_state.step = "email_gate"
    st.rerun()