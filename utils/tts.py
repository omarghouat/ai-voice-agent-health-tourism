from TTS.api import TTS
import simpleaudio as sa

# Initialize TTS model
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

def speak(text):
    tts.tts_to_file(text=text, file_path="output.wav")
    
    # Play audio
    wave_obj = sa.WaveObject.from_wave_file("output.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()
