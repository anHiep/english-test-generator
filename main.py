from termcolor import colored
from canvasapi import Canvas
from dotenv import load_dotenv
import csv
import os
import time
import traceback

from agentic_rag.client import get_ideas

load_dotenv()

API_URL = os.getenv("CANVAS_LMS_API_URL")
API_KEY = os.getenv("CANVAS_LMS_API_KEY")
COURSE_ID = os.getenv("COURSE_ID")

# Prepare output directories
print("...")
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
current_time = time.strftime("%Y%m%d_%H%M%S")
dist_path = os.path.join(output_dir, f"dist{current_time}")
os.makedirs(dist_path, exist_ok=True)
listening_dir = os.path.join(dist_path, "listening")
reading_dir = os.path.join(dist_path, "reading")
os.makedirs(listening_dir, exist_ok=True)
os.makedirs(reading_dir, exist_ok=True)

csv_path = f"course_progress/{COURSE_ID}/topic.csv"

def read_topics_csv():
    topics = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            topics.append({"topic": row["topic"], "last_index": int(row.get("last_index", 0))})
    return topics

def update_topic_progress(topic, new_index):
    rows = read_topics_csv()
    for row in rows:
        if row["topic"] == topic:
            row["last_index"] = new_index
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["topic", "last_index"])
        writer.writeheader()
        writer.writerows(rows)

def ensure_module_exists(topic: str):
    canvas = Canvas(API_URL, API_KEY)
    course = canvas.get_course(COURSE_ID)

    for module in course.get_modules():
        if module.name == topic:
            print(colored("[FOUND]", "green"), f"Module '{colored(topic, 'yellow')}' already exists.")
            if not module.published:
                module.edit(module={'published': True})
                print(colored("[UPDATED]", "blue"), f"Module '{colored(topic, 'yellow')}' was unpublished. Now published.")
            return module

    new_module = course.create_module(module={"name": topic})
    new_module.edit(module={'published': True})
    print(colored("[CREATED]", "magenta"), f"Created and published new module '{colored(topic, 'yellow')}'.")
    return new_module

def safe_quiz_creation(create_func, idea, idx, dist_path, topic, module):
    """Retry quiz creation until it succeeds."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            create_func(idea, idx + 1, dist_path, topic, module)
            return True
        except Exception as e:
            print(colored("[ERROR]", "red"), f"Idea {idx} for '{topic}' failed. Attempt {attempt + 1}/{max_retries}")
            print(traceback.format_exc())
            if attempt == max_retries - 1:
                return False
            time.sleep(5)
    return False

topics = read_topics_csv()

for entry in topics:
    topic = entry["topic"]
    start_index = entry["last_index"]

    if start_index == 10:
        continue

    print(colored("[RUNNING]", "blue"), f"Processing topic: {colored(topic, 'yellow')} (starting at idea {start_index})")
    module = ensure_module_exists(topic)

    print(colored("[RUNNING]", "blue"), "Generating ideas for English test.")
    raw_ideas = get_ideas(topic)
    ideas = raw_ideas.split(" | ")
    print(colored("[DONE]", "green"), "Complete generating ideas for English test.")

    file_path = os.path.join(dist_path, f"ideas.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        for idea in ideas:
            f.write(f"{idea}\n")
    print(colored("[DONE]", "green"), "Complete writing ideas to file:", colored(file_path, "yellow"))

    for idx in range(start_index, len(ideas)):
        idea = ideas[idx]
        try:
            from listeningA1A2.listening import create_listening_quiz
            ok = safe_quiz_creation(create_listening_quiz, idea, idx, dist_path, topic, module)
            # from listeningB1B2.listening import create_listening_quiz
            # ok = safe_quiz_creation(create_listening_quiz, idea, idx, dist_path, topic, module)
            # from listeningC1C2.listening import create_listening_quiz
            # ok = safe_quiz_creation(create_listening_quiz, idea, idx, dist_path, topic, module)

            if ok:
                update_topic_progress(topic, idx + 1)
                print(colored("[DONE]", "green"), f"Idea {idx} processed successfully for {topic}.")
            else:
                print(colored("[STOPPED]", "red"), f"Failed permanently at idea {idx} for {topic}. Resuming later.")
                break

        except Exception as e:
            print(colored("[FATAL]", "red"), f"Unexpected error at idea {idx} for {topic}: {e}")
            print(traceback.format_exc())
            update_topic_progress(topic, idx)
            break

print(colored("[DONE]", "green"), "All topics processed.")