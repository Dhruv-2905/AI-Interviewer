import requests
from Configuration.config import API_KEY, MODEL_NAME, BASE_URL, SYSTEM_PROMPT
import re

def generate_questions(topics: list, level: str):
    questions = {}
    for topic in topics:
        prompt = f"""
                Generate 5 interview questions based on the following criteria:

                - Topic: '{topic}'
                - Level: {level}

                Instructions:
                1. Only include theory-based or use case-based questions.
                2. Do NOT include any questions related to Data Structures, Algorithms, or coding.
                3. Ensure all questions are strictly based on the given topic only — do NOT include content from any other topic.
                4. Present the questions in a numbered list format (1 to 5).
                5. Just return the question list only, nothing else.
                """
        messages = [SYSTEM_PROMPT, {"role": "user", "content": prompt}]
        response = requests.post(
            BASE_URL,
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "max_tokens": 512,
                "temperature": 0.7
            },
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        data = response.json()
        if "choices" in data:
            content = data["choices"][0]["message"]["content"]
            questions[topic] = content.strip()
        else:
            questions[topic] = "Error generating questions."
    return questions

def evaluate_answer(question: str, answer: str) -> tuple:
    prompt = (
        f"The following is a user's answer to an interview question.\n\n"
        f"Question: {question}\n"
        f"Answer: {answer}\n\n"
        f"Please provide a short and concise evaluation of the answer."
        f" Return your evaluation and then the rating out of 10 in the format: [Evaluation text] Rating: [score]/10."
    )
    messages = [SYSTEM_PROMPT, {"role": "user", "content": prompt}]
    response = requests.post(
        BASE_URL,
        json={
            "model": MODEL_NAME,
            "messages": messages,
            "max_tokens": 300,
            "temperature": 0.5
        },
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    data = response.json()
    if "choices" in data:
        content = data["choices"][0]["message"]["content"].strip()
        score_match = re.search(r'(?i)(?:rating[:\s]*|)(\d{1,2})(?:/10)?', content)
        score = int(score_match.group(1)) if score_match else 5
        return content, score
    return "Could not evaluate answer.", 5

def explain_answer(question: str) -> str:
    prompt = (
        f"Give a brief, clear, concise, and complete explanation of the ideal answer to this question:\n"
        f"{question}"
    )
    messages = [SYSTEM_PROMPT, {"role": "user", "content": prompt}]
    response = requests.post(
        BASE_URL,
        json={
            "model": MODEL_NAME,
            "messages": messages,
            "max_tokens": 200,
            "temperature": 0.5
        },
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    data = response.json()
    if "choices" in data:
        return data["choices"][0]["message"]["content"].strip()
    return "Could not generate explanation."
