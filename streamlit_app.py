import streamlit as st
from groq import Groq
import os

# Page config - Render ke liye zaruri
st.set_page_config(
    page_title="ScopeAI - JEE/NEET Tutor", 
    page_icon="⭐",
    layout="centered"
)

# Header
st.markdown("<h1 style='text-align: center; color: #A78BFA;'>⭐ ScopeAI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9CA3AF;'>Free JEE/NEET AI Tutor by Groq</p>", unsafe_allow_html=True)
st.divider()

# Groq Client Setup - Error handle kiya hua
try:
    groq_api_key = os.environ["GROQ_API_KEY"]
    client = Groq(api_key=groq_api_key)
except KeyError:
    st.error("⚠️ GROQ_API_KEY nahi mili! Render > Environment mein add karo")
    st.stop()

# Chat history maintain karo
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purane messages dikhao
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User ka input lo
if prompt := st.chat_input("JEE/NEET ka sawal pucho..."):
    # User message save karo
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI ka jawab generate karo
    with st.chat_message("assistant"):
        with st.spinner("ScopeAI soch raha hai..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system", 
                            "content": "Tum ScopeAI ho, ek expert JEE/NEET tutor. Class 11-12 ke students ko Hinglish mein samjhao. Step by step, simple words mein. NCERT ke hisaab se padhao. Examples zarur do."
                        },
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    model="llama-3.1-8b-instant", # Latest working model
                    temperature=0.7,
                    max_tokens=2048,
                )
                
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                
                # Assistant message save karo
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"😅 Error aa gaya: {str(e)}")
                st.info("Model ka naam check karo ya API key sahi hai?")
