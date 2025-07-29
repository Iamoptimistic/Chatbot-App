
import streamlit as st
import difflib
pip install sentence-transformers

# Simple FAQ-style bot for Parvovirus Enteritis
st.set_page_config(page_title="ParvoBot", layout="centered")
st.title("🐶 ParvoBot: Ask me about Parvovirus Enteritis!")

# Sample Q&A knowledge base
faq = {
"what is parvoviral enteritis": "Parvoviral enteritis is a severe, highly contagious viral disease in dogs caused by canine parvovirus (CPV). It primarily affects the gastrointestinal tract, leading to symptoms such as vomiting, profuse bloody diarrhea, dehydration, lethargy, and, if untreated, can lead to death, especially in puppies.",

"what causes parvoviral enteritis": "The disease is caused by canine parvovirus type 2 (CPV-2), which has several variants including CPV-2a, CPV-2b, and CPV-2c. These variants are capable of infecting rapidly dividing cells, particularly in the intestinal lining, bone marrow, and lymphoid tissue, leading to immunosuppression and intestinal damage.",

"how is parvovirus transmitted": "Canine parvovirus is primarily transmitted through the fecal-oral route. Infected dogs shed the virus in their feces, and healthy dogs can become infected by ingesting the virus from contaminated environments, objects, or direct contact. The virus is extremely hardy and can survive in the environment for months.",

"which dogs are most at risk of parvovirus": "Unvaccinated dogs, especially puppies between 6 weeks and 6 months old, are at highest risk. Other risk factors include overcrowded living conditions (such as shelters or breeding facilities), poor nutrition, concurrent infections, and stress, all of which can compromise immune defense.",

"can parvovirus affect other animals or humans": "Parvovirus is species-specific, so canine parvovirus does not infect humans. However, cats can be affected by a closely related virus called feline panleukopenia virus. Dogs can only transmit parvovirus to other dogs.",

"what are the symptoms of parvoviral enteritis": "Symptoms include sudden onset of vomiting, foul-smelling bloody or watery diarrhea, fever or hypothermia, extreme lethargy, loss of appetite, abdominal pain, and rapid dehydration. Severe cases may lead to sepsis, shock, and death without prompt treatment.",

"how soon do symptoms appear after exposure": "Clinical signs usually develop within 3 to 7 days after exposure to the virus. The incubation period can vary depending on the viral load, immune status, and age of the dog.",

"how is parvovirus diagnosed": "Diagnosis is based on clinical signs, history of exposure or lack of vaccination, and confirmation using diagnostic tests like fecal ELISA antigen tests, PCR (polymerase chain reaction), or hemagglutination assays. Bloodwork often reveals leukopenia (low white blood cell count).",

"what does a complete blood count (CBC) show in parvo cases": "In affected dogs, the CBC typically shows leukopenia (a significant drop in white blood cells), indicating bone marrow suppression. Other findings may include anemia and hemoconcentration due to dehydration.",

"what is the treatment for parvoviral enteritis": "There is no antiviral cure for parvovirus, so treatment is supportive. This includes aggressive intravenous fluid therapy, electrolyte replacement, antiemetics to control vomiting, antibiotics to prevent or treat secondary bacterial infections, nutritional support, and close monitoring. Early intervention significantly improves survival.",

"can parvovirus be treated at home": "Home treatment is generally not recommended due to the severity of the disease and risk of rapid deterioration. Hospitalization is often necessary to provide IV fluids, medications, and constant monitoring. In some mild cases or where hospitalization is not possible, outpatient protocols may be attempted under veterinary guidance.",

"what is the prognosis for dogs with parvo": "With prompt and intensive care, survival rates can exceed 80-90%. However, in untreated or severely affected cases, especially in young puppies, the disease can be fatal. Prognosis depends on how quickly treatment is initiated, the dog’s immune response, and overall health status.",

"can recovered dogs get parvovirus again": "Most dogs that recover from parvovirus develop long-lasting, possibly lifelong immunity against the strain they were infected with. However, completing the full vaccination schedule is still strongly advised for comprehensive protection.",

"how can parvoviral enteritis be prevented": "The most effective method of prevention is vaccination. Puppies should begin vaccination at 6–8 weeks of age, followed by booster shots every 3–4 weeks until at least 16–20 weeks. Good hygiene, isolation of infected dogs, and disinfection of contaminated environments also help prevent spread.",

"what type of vaccine protects against parvovirus": "Modified live vaccines are used to protect dogs against parvovirus. These are highly effective and are often included in combination vaccines such as DHPP (Distemper, Hepatitis, Parvovirus, Parainfluenza).",

"how long does the parvovirus live in the environment": "Canine parvovirus is extremely hardy and resistant to heat, cold, and many disinfectants. It can survive in the environment for up to one year, especially in cool, moist areas. This makes environmental decontamination very important.",

"what disinfectants kill parvovirus": "Effective disinfectants include household bleach (sodium hypochlorite) diluted 1:30, accelerated hydrogen peroxide, and some veterinary-grade disinfectants like potassium peroxymonosulfate. These must be used correctly and allowed appropriate contact time to ensure efficacy.",

"can vaccinated dogs still get parvovirus": "While uncommon, vaccinated dogs can still contract parvovirus if they were not fully immunized, have an inadequate immune response, or are exposed to a very high viral load. However, disease severity is usually lower in vaccinated dogs.",

"how is parvovirus controlled in shelters or clinics": "Control measures include isolation of suspected or confirmed cases, strict sanitation protocols, vaccination of all incoming animals, use of protective clothing, and limiting foot traffic. Fomite transmission through shoes, equipment, and hands must also be addressed.",

"is parvovirus contagious to other dogs": "Yes, parvovirus is highly contagious among dogs. Even a small amount of contaminated fecal material can infect another dog. Infected dogs should be isolated until they are fully recovered and no longer shedding the virus.",

"how long does a dog shed parvovirus after recovery": "Dogs can continue shedding the virus in their feces for up to 10 days or more after clinical recovery. During this time, they can still infect other dogs, so strict isolation and hygiene are crucial even after symptoms resolve.",

"should I bring my puppy to the vet if I suspect parvo": "Yes. Parvovirus can progress rapidly, and early veterinary intervention is critical for survival. Delaying treatment significantly reduces the chance of recovery.",

"can parvovirus be spread by shoes or clothes": "Yes. The virus can be easily transported on shoes, clothes, hands, or equipment. Anyone exposed to an infected environment should disinfect thoroughly before handling other dogs or entering clean areas.",

"can my other pets get sick from an infected dog": "Parvovirus does not infect humans or species like cats or birds. However, other dogs in the household are at risk if they are not fully vaccinated. All surfaces, bedding, and items should be disinfected to prevent transmission."
}

from sentence_transformers import SentenceTransformer, util
import torch

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Prepare your FAQ
questions = list(faq_data.keys())
question_embeddings = model.encode(questions, convert_to_tensor=True)

def get_answer(user_input, threshold=0.6):
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    cosine_scores = util.cos_sim(user_embedding, question_embeddings)[0]

    top_result = torch.argmax(cosine_scores).item()
    top_score = cosine_scores[top_result].item()

    if top_score >= threshold:
        matched_question = questions[top_result]
        return faq_data[matched_question]
    else:
        return "Sorry, I don't know the answer to that yet. Try asking about symptoms, treatment, or prevention."

# Example usage
print(get_answer("what is parvo in dogs?"))  # Should match "what is parvovirus enteritis"


"""

# Get user input
user_input = st.text_input("Ask your question:")

if user_input:
    # Normalize user input
    user_question = user_input.lower().strip()

    # Find the closest match from the FAQ keys
    closest_match = difflib.get_close_matches(user_question, faq.keys(), n=1, cutoff=0.4)

    if closest_match:
        response = faq[closest_match[0]]
        st.success(response)
    else:
        st.warning("Sorry, I don't know the answer to that yet. Try rephrasing or asking about symptoms, causes, or prevention.")
"""
