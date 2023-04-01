import speech_recognition as sr

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
    transcription = recognizer.recognize_google(audio_data)
    return transcription
