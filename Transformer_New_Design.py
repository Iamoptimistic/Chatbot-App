import streamlit as st
import pandas as pd
import random
from sentence_transformers import SentenceTransformer, util

# Page config
st.set_page_config(page_title="PedsPulmoBot", layout="centered")

# Inject improved CSS
st.markdown("""
    <style>
        /* Reset top padding so title is visible */
        .main {
            padding-top: 120px !important;
            padding-bottom: 100px !important;
        }

        /* Sticky header */
        .title-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: white;
            z-index: 1000;
            padding: 1rem 1rem 0.5rem 1rem;
            border-bottom: 1px solid #ccc;
        }

        /* Chat messages container */
        .content-container {
            overflow-y: auto;
            max-height: 70vh;
            padding: 1rem 0.5rem;
            margin-bottom: 120px; /* Space for the input */
        }

        .footer-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: white;
            z-index: 1000;
            border-top: 1px solid #ccc;
            padding: 1rem;
        }

        .chat-message {
            margin-bottom: 0.75rem;
        }

        .user-message {
            color: black;
            font-weight: bold;
        }

        .bot-message {
            color: #2c3e50;
        }
    </style>
""", unsafe_allow_html=True)

# Fixed Title
st.markdown('<div class="title-container"><h2>PedsPulmoBot: Ask Me About Pediatric Pulmonary Diseases</h2></div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("👨‍⚕️ This bot is built by Abdulateef, Amaka and Agede")

# Load model
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("pediatric_pulmonology_QA_dataset_complete.csv")
    df["embedding"] = df["Question"].apply(lambda x: model.encode(str(x), convert_to_tensor=True))
    return df

faq = load_data()

# Disease Filter
disease_filter = st.sidebar.selectbox("🩺 Filter by Disease", ["All Diseases"] + sorted(faq["Disease"].unique()))

filtered_faq = faq if disease_filter == "All Diseases" else faq[faq["Disease"] == disease_filter].copy()

# Chat memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat area
st.markdown('<div class="content-container">', unsafe_allow_html=True)

for sender, message in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f'<div class="chat-message user-message">**You:** {message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message bot-message">**PedsPulmoBot:** {message}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input at bottom
st.markdown('<div class="footer-container">', unsafe_allow_html=True)
user_input = st.text_input("Type your question here:", key="chat_input", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# Handle input
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    user_embedding = model.encode(user_input, convert_to_tensor=True)

    similarities = [float(util.cos_sim(user_embedding, emb)) for emb in filtered_faq["embedding"]]
    filtered_faq["similarity"] = similarities
    best_match = filtered_faq.loc[filtered_faq["similarity"].idxmax()]

    if best_match["similarity"] > 0.4:
        response = random.choice([
            "Sure thing! ",
            "Great question. ",
            "Absolutely! ",
            "You got it! ",
        ]) + best_match["Answer"]
    else:
        response = "I'm not confident about that answer. Try asking a more specific question about a disease or topic."

    st.session_state.chat_history.append(("bot", response))
