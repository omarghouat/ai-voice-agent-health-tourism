import streamlit as st
from streamlit_webrtc import webrtc_streamer
from utils.stt import AudioProcessor
from utils.llm import generate_response
from utils.tts import speak

st.set_page_config(page_title="AI Voice Agent - Health Tourism", layout="centered")
st.title("🎤 AI Voice Agent for Health Tourism")
st.markdown("Ask about medical travel, clinics, procedures, visas, and more.")

# Create a placeholder to display results
result_placeholder = st.empty()

# Instantiate audio processor
processor = AudioProcessor(result_placeholder)

# Streamlit WebRTC component
webrtc_ctx = webrtc_streamer(
    key="voice-agent",
    mode="SENDONLY",
    in_audio=True,
    audio_frame_callback=processor.audio_callback,
    media_stream_constraints={"audio": True, "video": False}
)

# If user finishes speaking and we get processed text
if processor.transcript and not processor.responded:
    with st.spinner("🧠 Thinking..."):
        ai_response = generate_response(processor.transcript)
        result_placeholder.markdown(f"**🗣️ You said:** {processor.transcript}")
        st.write("🤖 Assistant:", ai_response)

        with st.spinner("🔊 Speaking..."):
            speak(ai_response)
            st.audio("output.wav", format="audio/wav")
        processor.responded = True

