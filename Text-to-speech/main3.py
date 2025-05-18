import requests
from gtts import gTTS
import pygame
import os
import tempfile

# Replace this with your Together.ai key
api_key = "b66be46fa968dd553942226972d5e6726a08b16a4839cd2d2a789c38f2cc644b"

# LLaMA 3 model
model = "meta-llama/Llama-3-8b-chat-hf"
chat_history = [
    {
        "role": "system",
        "content": "You are a friendly, human-like conversational bot. Respond naturally, as a person would, with short and concise answers. Avoid saying things like 'I'm just an AI' or mentioning your limitations. When asked about feelings or personal experiences, give warm, relatable responses."
    }
]

# Initialize pygame mixer for audio playback
pygame.mixer.init()

print("Chat with LLaMA 3 (Together.ai). Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    chat_history.append({"role": "user", "content": user_input})

    payload = {
        "model": model,
        "messages": chat_history,
        "max_tokens": 100,  # Reduced for concise responses
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.post("https://api.together.xyz/v1/chat/completions", json=payload, headers=headers)
    result = response.json()

    if "choices" in result:
        message = result["choices"][0]["message"]["content"]
        print("Bot:", message)

        # Generate speech with gTTS
        tts = gTTS(text=message, lang='en', slow=False)
        # Save to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            tts.save(temp_file.name)
            temp_file_path = temp_file.name

        # Play the audio
        pygame.mixer.music.load(temp_file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Clean up temporary file
        pygame.mixer.music.unload()
        os.remove(temp_file_path)

        chat_history.append({"role": "assistant", "content": message})
    else:
        print("Error:", result)

# Clean up pygame
pygame.mixer.quit()