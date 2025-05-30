import vosk
#import pyaudio
import av
import numpy as np

def listen():
    model = vosk.Model("model-en")  # Make sure this folder exists in root
    recognizer = vosk.KaldiRecognizer(model, 16000)

    #mic = pyaudio.PyAudio()
    stream = mic.open(rate=16000, format=pyaudio.paInt16, channels=1,
                      input=True, frames_per_buffer=8192)
    stream.start_stream()

    print("🎤 Listening...")
    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            return result[14:-3]  # Extract text from JSON result

    def audio_callback(frame: av.AudioFrame) -> av.AudioFrame:
    audio_data = frame.to_ndarray()
    # Here you can process or save the audio_data
    print("Audio shape:", audio_data.shape)
    return frame  # Must return the frame even if not modified

