from termcolor import colored
import os
import time
import json

from agentic_rag.client import get_ideas

print("...")
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
current_time = time.strftime("%Y%m%d_%H%M%S")
dist_path = os.path.join(output_dir, f"dist{current_time}")
os.makedirs(dist_path)

# print(colored("[RUNNING]", "blue"), "Generating ideas for English test.")
# raw_ideas = get_ideas("Space Exploration")
# ideas = raw_ideas.split(" | ")
# print(colored("[DONE]", "green"), "Complete generating ideas for English test.")

# print(colored("[RUNNING]", "blue"), "Writing ideas to file.")
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

for x in ideas: 
    print("-", x)

