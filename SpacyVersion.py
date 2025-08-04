import streamlit as st
import pandas as pd
import spacy
import random

# Set up Streamlit
st.set_page_config(page_title="PedsPulmoBot", layout="centered")
st.title("👶 PedsPulmoBot: Ask Me About Pediatric Pulmonology")
st.sidebar.markdown("🤖 Powered by spaCy NLP — Ask about asthma, CF, BPD, and more!")

# Load spaCy model
@st.cache_resource
def load_model():
    return spacy.load("en_core_web_md")

nlp = load_model()

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("pediatric_pulmonology_QA_dataset_complete.csv")
    df["doc"] = df["Question"].apply(lambda x: nlp(str(x)))
    return df

faq = load_data()

# Friendly wrapper
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

# User input box
user_input = st.text_input("You:", key="chat_input")

# Handle user input
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    user_doc = nlp(user_input)

    # Compute similarities
    faq["similarity"] = faq["doc"].apply(lambda doc: user_doc.similarity(doc))
    best_match = faq.sort_values(by="similarity", ascending=False).iloc[0]

    if best_match["similarity"] > 0.75:
        answer = best_match["Answer"]
        disease = best_match["Disease"]
        category = best_match["Category"]
        response = friendly_wrap(f"{answer} _(Disease: {disease}, Category: {category})_")
    else:
        response = "Hmm... I’m not quite sure about that. Try asking about causes, symptoms, or treatments of a specific disease."

    st.session_state.chat_history.append(("bot", response))

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**PedsPulmoBot:** {message}")
