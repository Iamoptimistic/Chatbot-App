import streamlit as st
import pandas as pd
import random
from sentence_transformers import SentenceTransformer, util

# Set page config
st.set_page_config(page_title="PedsPulmoBot", layout="centered")

# Load model and data
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

@st.cache_data
def load_data():
    df = pd.read_csv("pediatric_pulmonology_QA_dataset_complete.csv")
    df["embedding"] = df["Question"].apply(lambda x: model.encode(str(x), convert_to_tensor=True))
    return df

faq = load_data()

# Friendly response
def friendly_wrap(answer):
    openings = [
        "Sure thing! ",
        "Great question. ",
        "Absolutely! ",
        "Here's what I can tell you: ",
        "You got it! ",
    ]
    return random.choice(openings) + answer

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# CSS styling
st.markdown("""
    <style>
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #ddd;
        background-color: #0000FF;
        border-radius: 10px;
    }
    .user-bubble {
        background-color: #008000;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        margin-left: auto;
        max-width: 75%;
    }
    .bot-bubble {
        background-color: #E6E6E6;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        margin-right: auto;
        max-width: 75%;
    }
    .input-row {
        display: flex;
        gap: 10px;
    }
    .title-style {
        font-size: 100px;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #008000;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="title-style">🤖 PedsPulmoBot: Your Pediatric Pulmonology Assistant</p>', unsafe_allow_html=True)
st.markdown("Ask me about paediatric pulmonary diseases")

# Input box
user_input = st.text_input("Type your question here...", key="chat_input")

# Process input
if user_input:
    st.session_state.chat_history.append(("user", user_input))

    user_embedding = model.encode(user_input, convert_to_tensor=True)
    similarities = [float(util.cos_sim(user_embedding, emb)) for emb in faq["embedding"]]
    faq["similarity"] = similarities
    best_match = faq.loc[faq["similarity"].idxmax()]

    if best_match["similarity"] > 0.6:
        answer = best_match["Answer"]
        disease = best_match["Disease"]
        category = best_match["Category"]
        response = friendly_wrap(f"{answer}_")
    else:
        response = "I'm not sure about that yet. Try asking a more specific question about a disease or condition."

    st.session_state.chat_history.append(("bot", response))

# Display conversation
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for sender, message in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f'<div class="user-bubble">🧑‍⚕️ {message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">🤖 {message}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

