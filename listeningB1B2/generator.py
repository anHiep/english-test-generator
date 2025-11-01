from handler.llm import call_llm
from .prompt.listening_prompt import generate_listening_prompt

def generate_listening(idea: str):
    prompt = generate_listening_prompt(topic=idea)
    response = call_llm(prompt=prompt, openrouter=False, model_ollama="qwen3:8b")
    return response, prompt
