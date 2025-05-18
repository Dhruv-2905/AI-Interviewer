from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Falcon-RW-1B is small and works well on CPU
model_id = "tiiuae/falcon-rw-1b"

# Load the model and tokenizer (downloaded automatically and cached)
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Create a text generation pipeline
chatbot = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)

print("Chatbot ready. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    response = chatbot(user_input, max_new_tokens=150, do_sample=True, temperature=0.7)
    print("Bot:", response[0]["generated_text"].strip())
