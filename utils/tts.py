from gtts import gTTS

def speak(text):
    tts = gTTS(text)
    tts.save("output.wav")
