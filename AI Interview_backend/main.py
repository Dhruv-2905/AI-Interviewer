# main.py
from Interview.manage import conduct_virtual_interview
from Text_Speech.speech import cleanup

def main():
    print("Welcome to the Virtual Interview Agent!\n")
    topics_input = input("Enter topics (comma separated): ")
    level = input("Enter difficulty level (beginner/intermediate/advanced): ").strip()

    topics = [topic.strip() for topic in topics_input.split(',') if topic.strip()]
    if not topics:
        print("No valid topics provided. Exiting.")
        return

    conduct_virtual_interview(topics, level)
    cleanup()

if __name__ == "__main__":
    main()
