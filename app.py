import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import whisper
import tempfile
import os
from utils.llm import generate_response
from utils.tts import speak  # Make sure speak() saves to output.wav

# Whisper model
model = whisper.load_model("base")

st.set_page_config(page_title="AI Voice Agent - Health Tourism", layout="centered")

st.title("🎤 AI Voice Agent for Health Tourism")
st.markdown("Ask about medical travel, clinics, procedures, visas, and more.")

# AudioProcessor class
class AudioProcessor:
    def __init__(self):
        self.recording = b""

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray()
        self.recording += audio.tobytes()
        return frame

    def get_audio(self):
        return self.recording

# WebRTC Audio Stream
ctx = webrtc_streamer(
    key="speech",
    mode=WebRtcMode.SENDRECV,
    in_audio=True,
    client_settings=ClientSettings(
        media_stream_constraints={"audio": True, "video": False},
        rtc_configuration={},
    ),
    audio_processor_factory=AudioProcessor,
)

if st.button("🎙️ Process Speech"):
    if ctx and ctx.state.audio_processor:
        audio_data = ctx.state.audio_processor.get_audio()
        
        # Save audio to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_data)
            tmp_file_path = tmp_file.name

        # Transcribe with Whisper
        result = model.transcribe(tmp_file_path)
        user_input = result["text"]
        st.write("🗣️ You said:", user_input)

        # Generate LLM response
        ai_response = generate_response(user_input)
        st.write("🤖 Assistant:", ai_response)

        # TTS
        speak(ai_response)  # Save as "output.wav"
        st.audio("output.wav", format="audio/wav")

        os.remove(tmp_file_path)
