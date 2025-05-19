# tts.py
from gtts import gTTS
import pygame
import os
import tempfile

pygame.mixer.init()
AUDIO_FILE = os.path.join(tempfile.gettempdir(), "interview_bot_audio.mp3")

def speak(text):
    tts = gTTS(text=text, lang='en', tld='co.uk', slow=False)
    tts.save(AUDIO_FILE)
    pygame.mixer.music.load(AUDIO_FILE)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(30)

def cleanup():
    pygame.mixer.quit()
    if os.path.exists(AUDIO_FILE):
        os.remove(AUDIO_FILE)
