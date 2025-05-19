# config.py
API_KEY = ""
MODEL_NAME = "meta-llama/Llama-3-8b-chat-hf"
BASE_URL = "https://api.together.xyz/v1/chat/completions"

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are an intelligent interview bot. Ask thoughtful questions based on topics and difficulty. Avoid generic filler."
}
