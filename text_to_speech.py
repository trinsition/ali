from gtts import gTTS
import os
import uuid

def synthesize_speech(text):
    tts = gTTS(text)
    audio_filename = f"{uuid.uuid4()}.mp3"
    audio_path = os.path.join("audio", audio_filename)
    tts.save(audio_path)
