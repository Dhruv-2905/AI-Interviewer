import requests
from gtts import gTTS
import pygame
import os
import tempfile
import threading


# Replace this with your Together.ai key
api_key = "b66be46fa968dd553942226972d5e6726a08b16a4839cd2d2a789c38f2cc644b"

# LLaMA 3 model
model = "meta-llama/Llama-3-8b-chat-hf"
system_prompt = [
    {
        "role": "system",
        "content": "You are a friendly, human-like conversational bot. Respond naturally, as a person would, with short and concise answers. Avoid saying things like 'I'm just an AI' or mentioning your limitations. When asked about feelings or personal experiences, give warm, relatable responses."
    }
]

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Create a fixed temporary file for audio to reduce I/O overhead
temp_file_path = os.path.join(tempfile.gettempdir(), "chatbot_audio.mp3")

def generate_speech(text):
    """Generate and save TTS audio in a separate thread."""
    tts = gTTS(text=text, lang='en', tld='co.uk', slow=False)
    tts.save(temp_file_path)

print("Chat with LLaMA 3 (Together.ai). Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    # Create a fresh message list with only the system prompt and current input
    messages = system_prompt + [{"role": "user", "content": user_input}]

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 100,
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    # Make API call
    response = requests.post("https://api.together.xyz/v1/chat/completions", json=payload, headers=headers)
    result = response.json()

    if "choices" in result:
        message = result["choices"][0]["message"]["content"]
        print("Bot:", message)

        # Start TTS generation in a separate thread
        tts_thread = threading.Thread(target=generate_speech, args=(message,))
        tts_thread.start()
        tts_thread.join()  # Wait for TTS to complete before playback

        # Play the audio with minimal delay
        pygame.mixer.music.load(temp_file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(30)

        # Unload audio but keep file for reuse
        pygame.mixer.music.unload()
    else:
        print("Error:", result)

# Clean up
pygame.mixer.quit()
if os.path.exists(temp_file_path):
    os.remove(temp_file_path)