# utils/stt.py

import av
import numpy as np
import queue
import threading
import speech_recognition as sr
import wave

class AudioProcessor:
    def __init__(self, display):
        self.q = queue.Queue()
        self.transcript = None
        self.responded = False
        self.display = display
        self.recognizer = sr.Recognizer()
        self.audio_buffer = []
        self.started = False

    def audio_callback(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray()
        self.audio_buffer.append(audio)

        if not self.started:
            self.started = True
            threading.Thread(target=self.process_audio).start()

        return frame

    def process_audio(self):
        import time
        time.sleep(4)  # Wait a few seconds to capture full sentence

        audio_data = np.concatenate(self.audio_buffer, axis=1).flatten()
        audio_data = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)

        with wave.open("temp.wav", "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(48000)
            wf.writeframes(audio_data.tobytes())

        with sr.AudioFile("temp.wav") as source:
            audio = self.recognizer.record(source)
            try:
                self.transcript = self.recognizer.recognize_google(audio, language="en-US")
                self.display.markdown(f"**🗣️ You said:** {self.transcript}")
            except sr.UnknownValueError:
                self.display.markdown("🚫 Could not understand audio.")
            except sr.RequestError:
                self.display.markdown("⚠️ Could not reach the speech recognition service.")
