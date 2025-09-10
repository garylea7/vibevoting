import streamlit as st
from supabase import create_client, Client

# === SUPABASE SETUP ===
SUPABASE_URL = "https://bdcdqibdqomokoggjxzt.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJkY2RxaWJkcW9tb2tvZ2dqeHp0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc0MDk1NzksImV4cCI6MjA3Mjk4NTU3OX0.i7nUkRpJRB8u4bUxGn5Qztj_spYdvqLAdwdC8BtBfIA"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 'debate'
if 'vote' not in st.session_state:
    st.session_state.vote = None
if 'email' not in st.session_state:
    st.session_state.email = None
if 'referrer' not in st.session_state:
    st.session_state.referrer = st.query_params.get('referrer', '')
if 'friends_count' not in st.session_state:
    st.session_state.friends_count = 0

# === STEP 1: SHOW DEBATE ===
if st.session_state.step == 'debate':
    st.title("🥁 Do you LOVE or HATE drumming at sports games?")
    st.write("Vote first — unlock the secret: See who’s on your side.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("❤️ LOVE IT", use_container_width=True):
            st.session_state.vote = "love"
            st.session_state.step = "email_gate"
            st.rerun()
    with col2:
        if st.button("💢 HATE IT", use_container_width=True):
            st.session_state.vote = "hate"
            st.session_state.step = "email_gate"
            st.rerun()

# === STEP 2: SHOW EMAIL GATE ===
elif st.session_state.step == 'email_gate':
    st.title("🥁 Drumroll… Who’s on your side?")

    st.write("The crowd is split… but which side are YOUR friends on?")
    love_pct = 68
    hate_pct = 32

    st.progress(love_pct / 100)
    st.caption(f"❤️ {love_pct}% LOVE IT")

    st.progress(hate_pct / 100)
    st.caption(f"💢 {hate_pct}% HATE IT")

    st.write("🔓 Unlock your tribe + see if your friends agree with you.")
    email = st.text_input("Enter your email to reveal results", placeholder="you@example.com")

    if st.button("🔓 Unlock My Tribe + See Friends’ Votes", use_container_width=True):
        if email:
            # Save vote to Supabase
            supabase.table('votes').insert({
                'email': email,
                'vote': st.session_state.vote,
                'referrer': st.session_state.referrer
            }).execute()

            st.session_state.email = email

            # IF THERE'S A REFERRER, SAVE THE REFERRAL IMMEDIATELY
            if st.session_state.referrer:
                # Check if this referral already exists
                existing = supabase.table('referrals').select('*').eq('referrer_email', st.session_state.referrer).eq('referred_email', email).execute()
                if len(existing.data) == 0:
                    supabase.table('referrals').insert({
                        'referrer_email': st.session_state.referrer,
                        'referred_email': email
                    }).execute()

            # Count referrals for progress bar
            if st.session_state.referrer:
                ref_count = supabase.table('referrals').select('id').eq('referrer_email', st.session_state.referrer).execute()
                st.session_state.friends_count = len(ref_count.data)
            else:
                ref_count = supabase.table('referrals').select('id').eq('referred_email', email).execute()
                st.session_state.friends_count = len(ref_count.data)

            st.session_state.step = "share_to_unlock"
            st.rerun()
        else:
            st.warning("Please enter your email to continue.")

    st.info("🎁 First 100 voters get a free ‘I Survived the Drums’ digital badge 🎖️")