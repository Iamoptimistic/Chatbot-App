import streamlit as st
import pandas as pd
import random
from sentence_transformers import SentenceTransformer, util

# Page config
st.set_page_config(page_title="PedsPulmoBot", layout="centered")

# Inject custom CSS for sticky header and footer
st.markdown("""
    <style>
        /* Sticky header */
        .title-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background: white;
            z-index: 999;
            padding-top: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #ddd;
        }

        /* Push content below the title */
        .content-container {
            padding-top: 100px;
            padding-bottom: 100px;
        }

        /* Sticky footer */
        .footer-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: white;
            padding: 1rem;
            border-top: 1px solid #ddd;
            z-index: 999;
        }

        /* Chat messages styling */
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

# Load model (cached)
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# Load data and precompute embeddings (cached)
@st.cache_data
def load_data():
    df = pd.read_csv("pediatric_pulmonology_QA_dataset_complete.csv")
    df["embedding"] = df["Question"].apply(lambda x: model.encode(str(x), convert_to_tensor=True))
    return df

faq = load_data()

# Disease Filter
disease_filter = st.sidebar.selectbox("🩺 Filter by Disease", ["All Diseases"] + sorted(faq["Disease"].unique()))

if disease_filter != "All Diseases":
    filtered_faq = faq[faq["Disease"] == disease_filter].copy()
else:
    filtered_faq = faq.copy()

# Friendly response wrapper
def friendly_wrap(answer):
    openings = [
        "Sure thing! ",
        "Great question. ",
        "Absolutely! ",
        "You got it! ",
    ]
    return random.choice(openings) + answer

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Content container
st.markdown('<div class="content-container">', unsafe_allow_html=True)

# Display chat messages
for sender, message in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f'<div class="chat-message user-message">**You:** {message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message bot-message">**PedsPulmoBot:** {message}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Fixed Footer (Input box)
with st.container():
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
        response = friendly_wrap(best_match["Answer"])
    else:
        response = "I'm not confident about that answer. Try asking a more specific question about a disease or topic."

    st.session_state.chat_history.append(("bot", response))
    st.experimental_rerun()

