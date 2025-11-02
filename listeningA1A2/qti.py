from termcolor import colored
import subprocess
import sys
import os
import random
from time import sleep
from pydub import AudioSegment
from .tts import tts_model
from handler.llm import call_llm

from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Literal

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL")

MAX_RETRIES = 5
RETRY_DELAY = 3

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

class message(BaseModel):
    gender: Literal["male", "female"]
    name: str
    text: str

class question_stem(BaseModel):
    question: str
    answers: list[str]

class format(BaseModel):
    context: str
    question_quantity_guidance: str
    dialogue_part1: list[message]
    dialogue_part2: list[message]
    questions: list[question_stem]

def generate_qti(content: str, quiz_idx: int, topic: str):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(colored("[RUNNING]", "blue"), f"Attempt {attempt} of {MAX_RETRIES}")

            with open("listeningA1A2/prompt/format.txt", "r", encoding="utf-8") as f:
                prompt = f.read()

            print(colored("[RUNNING]", "blue"), "Requesting structured response from LLM...")
            completion = client.beta.chat.completions.parse(
                model=LLM_MODEL,
                messages=[
                    {"role": "user", "content": f"This is the IELTS Listening content: {content}"},
                    {"role": "user", "content": prompt},
                ],
                response_format=format,
            )
            response = completion.choices[0].message.parsed
            print(colored("[DONE]", "green"), "Received structured response from LLM.")

            qtiCode = f"Quiz title: [{topic}] Listening Level A1-A2 Quiz {quiz_idx}\n"

            qtiCode += f"\nText: {response.context}\n\n"

            qtiCode += f"Text: Listen carefully and answer questions one to five. Write **{response.question_quantity_guidance}** for each answer.\n\n"

            for quiz_num, q in enumerate(response.questions, 1):
                seen = set()
                unique_answers = [a for a in q.answers if not (a in seen or seen.add(a))]

                qtiCode += f"{quiz_num}. {q.question}\n"
                if quiz_num == 1:
                    for idx, msg in enumerate(response.dialogue_part1, 1):
                        prefix = "..." if idx == 1 else "    "
                        qtiCode += f"{prefix} {msg.name}: {msg.text}\n\n"
                    for msg in response.dialogue_part2:
                        qtiCode += f"    {msg.name}: {msg.text}\n\n"
                for ans in unique_answers:
                    qtiCode += f"*   {ans}\n"
                qtiCode += "\n"

                if quiz_num == 5:
                    qtiCode += f"Text: Listen carefully and answer questions six to ten. Write **{response.question_quantity_guidance}** for each answer.\n\n"

            output_path = "qti.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(qtiCode)
            print(colored("[DONE]", "green"), "Saved QTI file to:", colored(output_path, "yellow"))

            print(colored("[RUNNING]", "blue"), "Converting QTI text to Canvas format...")
            result = subprocess.run(
                ["text2qti", "qti.txt"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode != 0:
                print(colored("[ERROR]", "red"), "text2qti failed:")
                print(colored(result.stderr.strip(), "yellow"))
                raise RuntimeError("QTI conversion failed")
            print(colored("[DONE]", "green"), "QTI conversion complete.")

            # TTS Generation
            print(colored("[RUNNING]", "blue"), "Preparing to generate TTS audio...")

            final_audio = AudioSegment.silent(duration=0)
            female_voices = ["female_middle_age_1", "female_middle_age_2"]
            male_voices = ["male_middle_age_1", "male_young"]
            narrator_voice = "narrator"

            first_gender = response.dialogue_part1[0].gender
            second_gender = response.dialogue_part1[1].gender

            first_voice = random.choice(male_voices if first_gender == "male" else female_voices)
            second_voice = random.choice(male_voices if second_gender == "male" else female_voices)

            if first_voice == second_voice:
                pool = male_voices if second_gender == "male" else female_voices
                second_voice = random.choice([v for v in pool if v != first_voice])

            print(colored("[INFO]", "cyan"), f"First voice:  {first_voice} ({first_gender})")
            print(colored("[INFO]", "cyan"), f"Second voice: {second_voice} ({second_gender})")

            temp_audio_path = "temp.mp3"
            tts_model(response.context, narrator_voice)
            tts_audio = AudioSegment.from_file(temp_audio_path, format="mp3")
            os.remove(temp_audio_path)
            final_audio += tts_audio
            final_audio += AudioSegment.silent(duration=3000)

            print(colored("[RUNNING]", "blue"), "Synthesizing dialogue Part 1...")
            for idx, line in enumerate(response.dialogue_part1, 1):
                voice = first_voice if idx % 2 == 1 else second_voice
                temp_audio_path = "temp.mp3"
                tts_model(line.text, voice)
                tts_audio = AudioSegment.from_file(temp_audio_path, format="mp3")
                os.remove(temp_audio_path)
                final_audio += AudioSegment.silent(duration=500)
                final_audio += tts_audio
            print(colored("[DONE]", "green"), "Part 1 TTS complete.")

            temp_audio_path = "temp.mp3"
            tts_model("You will now have ten seconds to check your answers.", narrator_voice)
            tts_audio = AudioSegment.from_file(temp_audio_path, format="mp3")
            os.remove(temp_audio_path)
            final_audio += tts_audio
            final_audio += AudioSegment.silent(duration=10000)

            temp_audio_path = "temp.mp3"
            tts_model("Now listen carefully and answer questions six to ten.", narrator_voice)
            tts_audio = AudioSegment.from_file(temp_audio_path, format="mp3")
            os.remove(temp_audio_path)
            final_audio += tts_audio
            final_audio += AudioSegment.silent(duration=3000)

            print(colored("[RUNNING]", "blue"), "Synthesizing dialogue Part 2...")
            for idx, line in enumerate(response.dialogue_part2, 1):
                voice = first_voice if idx % 2 == 1 else second_voice
                temp_audio_path = "temp.mp3"
                tts_model(line.text, voice)
                tts_audio = AudioSegment.from_file(temp_audio_path, format="mp3")
                os.remove(temp_audio_path)
                final_audio += AudioSegment.silent(duration=500)
                final_audio += tts_audio
            print(colored("[DONE]", "green"), "Part 2 TTS complete.")

            # Adjust playback speed
            speed_factor = 1.05
            final_audio = final_audio._spawn(
                final_audio.raw_data,
                overrides={"frame_rate": int(final_audio.frame_rate * speed_factor)},
            ).set_frame_rate(final_audio.frame_rate)

            final_audio.export("audio.mp3", format="mp3")
            print(colored("[DONE]", "green"), "Exported audio to:", colored("audio.mp3", "yellow"))
            print(colored("[INFO]", "cyan"), f"Speed factor: {speed_factor}x")

            print(colored("[SUCCESS]", "green"), "generate_qti completed successfully.")
            break

        except Exception as e:
            print(colored("[ERROR]", "red"), f"Attempt {attempt} failed:", colored(str(e), "yellow"))
            if attempt < MAX_RETRIES:
                print(colored("[RETRY]", "magenta"), f"Retrying in {RETRY_DELAY}s...\n")
                sleep(RETRY_DELAY)
            else:
                print(colored("[FAILED]", "red"), "All attempts failed. Aborting.\n")