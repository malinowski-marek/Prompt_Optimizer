import json
import os
import re
import time
import random

# Attempt to import Streamlit for web UI; fallback to CLI if unavailable
try:
    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt
    IS_STREAMLIT = True
except ImportError:
    IS_STREAMLIT = False

# --- Configuration ---
STATS_FILE = 'stats.json'
COST_PER_TOKEN = 0.00002  # Adjust as needed ($)
# Simulate that there are already some savings till date
INITIAL_STATS = {
    'total_tokens_saved': 12345,
    'total_cost_saved': 246.90
}
# Path to LeanPrompt logo
LOGO_PATH = 'logo_light_transparent.png'

# --- Helper functions ---
def load_stats():
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return INITIAL_STATS.copy()

def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f)

def count_tokens(text):
    return len(text.split())

def simulate_granite(prompt, preserve_politeness=True, aggressiveness='medium'):
    latency = random.uniform(0.1, 0.3)
    time.sleep(latency)
    optimized = prompt
    if not preserve_politeness:
        optimized = re.sub(r"\b(please|kindly|thank you|thanks)\b", '', optimized, flags=re.IGNORECASE)
    polite_phrases = [
        r"\b(hello|dear|assistant)\b",
        r"I hope you[’']?re doing well\.",
        r"I[’']d be very grateful if you could",
        r"so much for your help"
    ]
    for pattern in polite_phrases:
        optimized = re.sub(pattern, '', optimized, flags=re.IGNORECASE)
    optimized = re.sub(r"!+", '', optimized)
    replacements = {
        'at this point in time': 'now',
        'in the event that': 'if',
        'with regard to': 'about',
        'due to the fact that': 'because',
        'in order to': 'to',
        'as a matter of fact': 'in fact'
    }
    for phrase, short in replacements.items():
        if aggressiveness in ('medium', 'aggressive'):
            optimized = re.sub(re.escape(phrase), short, optimized, flags=re.IGNORECASE)
    optimized = re.sub(r"\s*,\s*", ', ', optimized)
    optimized = re.sub(r",\s*,+", ',', optimized)
    optimized = re.sub(r"\s+", ' ', optimized)
    optimized = optimized.strip(' ,')
    return optimized, latency

def process_prompt(prompt, preserve, aggr, stats):
    orig_tokens = count_tokens(prompt)
    optimized, latency = simulate_granite(prompt, preserve_politeness=preserve, aggressiveness=aggr)
    new_tokens = count_tokens(optimized)
    saved_tokens = orig_tokens - new_tokens
    saved_cost = saved_tokens * COST_PER_TOKEN
    stats['total_tokens_saved'] += saved_tokens
    stats['total_cost_saved'] += saved_cost
    save_stats(stats)
    return {
        'original_tokens': orig_tokens,
        'optimized_text': optimized,
        'optimized_tokens': new_tokens,
        'tokens_saved': saved_tokens,
        'cost_saved': saved_cost,
        'latency': latency,
        'total_tokens_saved': stats['total_tokens_saved'],
        'total_cost_saved': stats['total_cost_saved']
    }

# --- CLI Version ---
if not IS_STREAMLIT:
    print("LeanPrompt Demo (CLI mode)")
    stats = load_stats()
    print(f"Starting with simulated total savings: {stats['total_tokens_saved']} tokens, ${stats['total_cost_saved']:.2f}\n")
    while True:
        prompt = input("Enter verbose prompt (or 'exit' to quit): ")
        if prompt.lower() in ('exit', 'quit'):
            break
        pref = input("Preserve politeness? (y/N): ")
        preserve = pref.strip().lower() == 'y'
        aggr = input("Aggressiveness (gentle/medium/aggressive): ") or 'medium'
        result = process_prompt(prompt, preserve, aggr, stats)
        print(f"\nOptimized Prompt: {result['optimized_text']}")
        print(f"Tokens saved: {result['tokens_saved']}, Cost saved: ${result['cost_saved']:.5f}")
        print(f"Simulated latency: {result['latency']:.2f}s")
        print(f"Total tokens saved: {result['total_tokens_saved']}, Total cost saved: ${result['total_cost_saved']:.5f}\n")
    print("Goodbye!")
    exit(0)

# --- Streamlit Web App ---
st.set_page_config(page_title="LeanPrompt", page_icon=LOGO_PATH, layout="wide")
# Dark theme CSS
st.markdown(
    '''
    <style>
    body { background-color: #0e1117; color: #fafafa; }
    .stApp { background-color: #0e1117; color: #fafafa; }
    .css-ffhzg2 img { background-color: transparent !important; }
    </style>
    ''', unsafe_allow_html=True
)

# Load state and stats
stats = load_stats()
view = st.sidebar.radio("Select View", ["Optimize", "Summary"])

if view == "Optimize":
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        st.image(LOGO_PATH, width=200)
    with col_title:
        st.title("LeanPrompt — Prompt Optimization & Cost Savings")
        st.write("Strip unnecessary words, minimize tokens, and save cost & energy.")
    preserve = st.sidebar.checkbox("Preserve Politeness", value=False)
    aggr = st.sidebar.selectbox("Aggressiveness", ['gentle', 'medium', 'aggressive'])
    st.sidebar.write(f"Cost per token: ${COST_PER_TOKEN:.5f}")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Your Prompt")
        prompt = st.text_area("Enter verbose prompt:", height=200)
        if st.button("Optimize Prompt"):
            if not prompt.strip():
                st.error("Please enter a prompt.")
            else:
                res = process_prompt(prompt, preserve, aggr, stats)
                st.session_state.res = res
        st.metric("Total Tokens Saved", stats['total_tokens_saved'])
        st.metric("Total Cost Saved", f"${stats['total_cost_saved']:.2f}")
    with col2:
        st.subheader("Optimized Prompt & Savings")
        if 'res' in st.session_state:
            res = st.session_state.res
            st.text_area("Optimized prompt:", value=res['optimized_text'], height=200)
            st.metric("Tokens Saved (this run)", res['tokens_saved'])
            st.metric("Cost Saved (this run)", f"${res['cost_saved']:.5f}")
            st.metric("Latency (s)", f"{res['latency']:.2f}")
        else:
            st.write("Optimize a prompt to see results here.")

elif view == "Summary":
    st.header("Cost Savings Summary")
    st.metric("Total Tokens Saved", stats['total_tokens_saved'])
    st.metric("Total Cost Saved", f"${stats['total_cost_saved']:.2f}")
    dates = pd.date_range(end=pd.Timestamp.today(), periods=7).strftime('%Y-%m-%d')
    tokens = [random.randint(100, 500) for _ in range(7)]
    costs = [t * COST_PER_TOKEN for t in tokens]
    df = pd.DataFrame({'Date': dates, 'Tokens Saved': tokens, 'Cost Saved ($)': costs})
    st.subheader("Last 7 Days Breakdown")
    st.dataframe(df, use_container_width=True)
        # Charts for executive summary: bar charts
    # Tokens saved over last 7 days
    fig1, ax1 = plt.subplots()
    ax1.bar(dates, tokens)
    ax1.set_title('Tokens Saved Over Last 7 Days')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Tokens Saved')
    plt.xticks(rotation=45)
    st.subheader('Tokens Saved Over Time')
    st.pyplot(fig1)

    # Cost saved over last 7 days
    fig2, ax2 = plt.subplots()
    ax2.bar(dates, costs)
    ax2.set_title('Cost Saved Over Last 7 Days')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Cost Saved ($)')
    plt.xticks(rotation=45)
    st.subheader('Cost Saved Over Time')
    st.pyplot(fig2)

st.write("---")
st.write("*Demo simulates IBM Granite. Replace simulate_granite with real API calls for production.*")
