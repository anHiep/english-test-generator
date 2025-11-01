from termcolor import colored
from canvasapi import Canvas
from dotenv import load_dotenv
import subprocess
import os
import time
import json

from agentic_rag.client import get_ideas

load_dotenv()

API_URL = os.getenv("CANVAS_LMS_API_URL")
API_KEY = os.getenv("CANVAS_LMS_API_KEY")
COURSE_ID = os.getenv("COURSE_ID")

print("...")
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
current_time = time.strftime("%Y%m%d_%H%M%S")
dist_path = os.path.join(output_dir, f"dist{current_time}")
os.makedirs(dist_path)
listening_dir = os.path.join(dist_path, "listening")
reading_dir = os.path.join(dist_path, "reading")
os.makedirs(listening_dir, exist_ok=True)
os.makedirs(reading_dir, exist_ok=True)

def ensure_module_exists(topic: str):
    canvas = Canvas(API_URL, API_KEY)
    course = canvas.get_course(COURSE_ID)

    for module in course.get_modules():
        if module.name == topic:
            print(colored("[FOUND]", "green"), f"Module '{colored(topic, 'yellow')}' already exists with ID {colored(module.id, 'cyan')}.")
            if not module.published:
                module.edit(module={'published': True})
                print(colored("[UPDATED]", "blue"), f"Module '{colored(topic, 'yellow')}' was unpublished. Now published.")
            return module

    new_module = course.create_module(module={"name": topic})
    new_module.edit(module={'published': True})
    print(colored("[CREATED]", "magenta"), f"Created and published new module '{colored(topic, 'yellow')}' with ID {colored(new_module.id, 'cyan')}.")
    return new_module

with open('topic.txt', 'r') as file:
    topics = file.read().splitlines()

for topic in topics:
    print(colored("[RUNNING]", "blue"), "Processing topic:", colored(topic, "yellow"))
    module = ensure_module_exists(topic)

    # print(colored("[RUNNING]", "blue"), "Generating ideas for English test.")
    # raw_ideas = get_ideas(topic)
    # ideas = raw_ideas.split(" | ")
    # print(colored("[DONE]", "green"), "Complete generating ideas for English test.")

    # file_path = os.path.join(dist_path, "ideas.txt")
    # with open(file_path, "w", encoding="utf-8") as f:
    #     if isinstance(ideas, dict):
    #         for k, v in ideas.items():
    #             f.write(f"{k}: {v}\n")
    #     elif isinstance(ideas, (list, tuple, set)):
    #         for item in ideas:
    #             f.write(f"{item}\n")
    #     else:
    #         if isinstance(ideas, str):
    #             for line in ideas.splitlines():
    #                 f.write(line + "\n")
    #         else:
    #             f.write(str(ideas) + "\n")
    # print(colored("[DONE]", "green"), "Complete writing ideas to file:", colored(dist_path, "yellow"))

    ideas = [
        "Debate the ethics of Mars colonization using terms like sustainability, resource allocation, and intergenerational equity",
        "Explain cosmic radiation protection measures with vocabulary like shielding, radiation exposure, and health risks"
    ]

    for idx, idea in enumerate(ideas):
        from listening.listening import create_listening_quiz
        create_listening_quiz(idea, idx + 1, dist_path, topic, module)

