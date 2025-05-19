# config.py
API_KEY = "b66be46fa968dd553942226972d5e6726a08b16a4839cd2d2a789c38f2cc644b"
MODEL_NAME = "meta-llama/Llama-3-8b-chat-hf"
BASE_URL = "https://api.together.xyz/v1/chat/completions"

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are an intelligent interview bot. Ask thoughtful questions based on topics and difficulty. Avoid generic filler."
}
