import streamlit as st
from utils.stt import listen
from utils.llm import generate_response
from utils.tts import speak

st.set_page_config(page_title="AI Voice Agent - Health Tourism", layout="centered")

st.title("🎤 AI Voice Agent for Health Tourism")
st.markdown("Ask about medical travel, clinics, procedures, visas, and more.")

if st.button("🎙️ Speak Now"):
    with st.spinner("👂 Listening..."):
        user_input = listen()
        st.write("🗣️ You said:", user_input)

        with st.spinner("🧠 Thinking..."):
            ai_response = generate_response(user_input)
            st.write("🤖 Assistant:", ai_response)

            with st.spinner("🔊 Speaking..."):
                speak(ai_response)
                st.audio("output.wav", format="audio/wav")
