
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
faq = {
    "what is parvoviral enteritis": "Parvoviral enteritis is a serious and highly contagious disease that affects dogs, especially puppies. It attacks their digestive system and causes vomiting, bloody diarrhea, and dehydration. Without treatment, it can be life-threatening.",
    "how is parvovirus transmitted": "Parvovirus spreads mainly through contact with infected dog feces. It can also be carried on shoes, hands, and objects. It's very tough and can survive in the environment for months!",
    "what are the symptoms of parvovirus": "Dogs with parvo often have vomiting, foul-smelling diarrhea (sometimes bloody), loss of appetite, lethargy, and fever. Puppies can get very sick very quickly.",
    "how can it be prevented": "Vaccination is key! Puppies need a series of shots starting around 6–8 weeks of age. Also, good hygiene and keeping sick dogs away from healthy ones helps a lot.",
}

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
