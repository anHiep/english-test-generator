from typing import List, Dict
import requests
from openai import OpenAI
import subprocess
import json
import re

OPENROUTER_API_KEY = "sample"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def call_openrouter(prompt: str, model: str = "openai/gpt-4o-mini") -> str:
    default_messages: List[Dict[str, str]] = [
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "assistant", "content": "Hello! How can I assist you today?"},
        {"role": "user", "content": "Hello!"},
    ]

    messages = [m.copy() for m in default_messages]
    if messages and messages[-1].get("role") == "user":
        messages[-1]["content"] = prompt
    else:
        messages.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return completion.choices[0].message.content

def run_local_llm(prompt: str, model: str = "qwen3") -> str:
    cmd = ["ollama", "run", model, prompt]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    output = proc.stdout.strip() or proc.stderr.strip()

    cleaned = re.sub(r"(?s)Thinking\.\.\..*?\.{3}done thinking\.?", "", output).strip()

    return cleaned

def call_llm(prompt: str, openrouter: bool = False, model_openrouter: str = "openai/gpt-4o-mini", model_ollama: str = "qwen3") -> str:
    if openrouter:
        return call_openrouter(prompt, model=model_openrouter)
    else:
        return run_local_llm(prompt, model=model_ollama)