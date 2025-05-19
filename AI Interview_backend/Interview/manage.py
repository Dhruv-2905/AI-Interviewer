import re
from Agent.llama_prompt import generate_questions, evaluate_answer, explain_answer
from statistics import mean

def generate_report(report: list):
    print("\n" + "="*60)
    print("\U0001F4C4 FINAL INTERVIEW REPORT")
    print("="*60)

    scores = []

    for i, item in enumerate(report, 1):
        print(f"\nQ{i}: {item['question']}")
        print(f"\U0001F5E3️  Your Answer : {item['user_answer']}")
        print(f"\U0001F4A1 Explanation : {item['explanation']}")
        print(f"\U0001F3C5 Score       : {item['score']}/10")
        scores.append(item['score'])

    average = round(mean(scores), 2) if scores else 0
    print("\n" + "="*60)
    print(f"\U0001F3AF OVERALL AVERAGE SCORE: {average}/10")
    print("="*60)


def conduct_virtual_interview(topics: list, level: str):
    all_questions = generate_questions(topics, level)
    report = []

    print("\nInterview starting...\n")

    for topic, questions_text in all_questions.items():
        print(f"\n--- Topic: {topic} ---\n")

        questions = re.findall(r'\d+\.\s.*?(?=\n\d+\.|\Z)', questions_text, re.DOTALL)

        if not questions:
            print("No valid questions found. Raw text:\n", questions_text)
            continue

        for i, question in enumerate(questions, 1):
            print(f"Q{i}: {question.strip()}")
            user_answer = input("Your answer: ").strip()

            print("\U0001F50D Evaluating your answer...")
            feedback, score = evaluate_answer(question, user_answer)
            explanation = explain_answer(question)

            # Extract score explicitly if present in feedback
            extracted_score = re.search(r'(\d+)/10', feedback)
            if extracted_score:
                score = int(extracted_score.group(1))
                feedback = re.sub(r'(\d+/10)', '', feedback).strip()

            report.append({
                "question": question.strip(),
                "user_answer": user_answer,
                "explanation": explanation,
                "score": score
            })

            print(f"\U0001F9E0 Feedback: {feedback}")
            print(f"✅ Score: {score}/10\n")

    generate_report(report)