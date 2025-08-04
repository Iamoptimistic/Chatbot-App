import streamlit as st
import pandas as pd
import difflib
import random

st.set_page_config(page_title="PedsPulmoBot", layout="centered")
st.title("👶 PedsPulmoBot: Chat About Pediatric Pulmonary Diseases")
st.sidebar.markdown("Ask me about childhood asthma, bronchopulmonary dysplasia, cystic fibrosis, and more!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

faq = pd.read_csv("pediatric_pulmonology_QA_dataset_complete.csv")

def friendly_wrap(answer):
    openings = [
        "Sure thing! ",
        "Great question. ",
        "Absolutely! ",
        "Here's what I can tell you: ",
        "You got it! ",
    ]
    return random.choice(openings) + answer

user_input = st.text_input("You:", key="chat_input")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    user_question = user_input.lower().strip()
    questions = faq["Question"].tolist()
    closest_match = difflib.get_close_matches(user_question, questions, n=1, cutoff=0.5)

    if closest_match:
        matched_row = faq[faq["Question"] == closest_match[0]]
        answer = matched_row["Answer"].values[0]
        disease = matched_row["Disease"].values[0]
        category = matched_row["Category"].values[0]
        response = friendly_wrap(f"{answer} _(Disease: {disease}, Category: {category})_")
    else:
        response = "Hmm... I’m not sure about that yet. Try asking about symptoms, causes, or treatments."

    st.session_state.chat_history.append(("bot", response))

for sender, message in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**PedsPulmoBot:** {message}")
```

---




"""

import streamlit as st
import difflib
import random

# Set up the page
st.set_page_config(page_title="ParvoBot", layout="centered")
st.title("🐶 ParvoBot: Let's Chat About Canine Parvovirus!")

st.sidebar.markdown("👋 Hi! I'm **ParvoBot**, your friendly vet assistant. Ask me anything about parvoviral enteritis in dogs!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Knowledge base (shortened for example)
faq = pd.read_csv("parvovirus_dataset_expanded.csv")


# Friendly response wrappers
def friendly_wrap(answer):
    openings = [
        "Sure thing! ",
        "Great question. ",
        "Absolutely! ",
        "Here's what I can tell you: ",
        "You got it! ",
    ]
    return random.choice(openings) + answer

# User input box
user_input = st.text_input("You:", key="chat_input")

# Process user input
if user_input:
    # Save user message
    st.session_state.chat_history.append(("user", user_input))

    # Fuzzy match input to known questions
    user_question = user_input.lower().strip()
    closest_match = difflib.get_close_matches(user_question, faq.keys(), n=1, cutoff=0.5)

    if closest_match:
        answer = faq[closest_match[0]]
        response = friendly_wrap(answer)
    else:
        response = "Hmm... I’m not sure about that yet. Try asking about symptoms, causes, or how to prevent parvovirus."

    # Save bot response
    st.session_state.chat_history.append(("bot", response))

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**ParvoBot:** {message}")
