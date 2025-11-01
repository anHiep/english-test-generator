from handler.llm import call_llm
from listening.prompt.listening_part1_prompt import generate_listening_part1_prompt

def generate_listening_part1(idea: str):
    prompt = generate_listening_part1_prompt(topic=idea)
    response = call_llm(prompt=prompt, openrouter=False, model_ollama="qwen3:8b")
    return response, prompt
