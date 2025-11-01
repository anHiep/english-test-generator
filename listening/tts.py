import torchaudio as ta
import torch
from chatterbox.tts import ChatterboxTTS
import uuid
import re
import os
import subprocess
import soundfile as sf

model = ChatterboxTTS.from_pretrained(device="cuda")

voices = {
    "female_middle_age_1": "Giọng nữ trung niên 1",
    "female_middle_age_2": "Giọng nữ trung niên 2",
    "male_middle_age_1": "Giọng nam trung niên 1",
    "male_old_1": "Giọng nam già 1",
}

def split_into_sentences(text: str):
    sentence_endings = re.compile(r'(?<=[.!?])\s+')
    sentences = sentence_endings.split(text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]

    chunks = []
    current_chunk = []
    current_words = 0
    current_chars = 0

    for sentence in sentences:
        word_count = len(sentence.split())
        char_count = len(sentence)

        if (current_words + word_count > 90) or (current_chars + char_count > 500):
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_words = word_count
            current_chars = char_count
        else:
            current_chunk.append(sentence)
            current_words += word_count
            current_chars += char_count

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def generate_tts_chunks(text: str, voice: str):
    audio_prompt_path = f"listening/voices/{voice}.wav"
    chunks = split_into_sentences(text)

    print(f"Splitting into {len(chunks)} chunk(s)")
    audio_segments = []

    for i, sentence in enumerate(chunks):
        print(f"Generating audio for chunk {i+1}")
        wav = model.generate(sentence, audio_prompt_path=audio_prompt_path)
        audio_segments.append(wav)

    full_audio = torch.cat(audio_segments, dim=1)
    return full_audio

def tts_model(text: str, voice: str):
    wav = generate_tts_chunks(text, voice)
    wav = wav.cpu().numpy().T  # torchaudio uses [channels, samples]
    sf.write("temp.wav", wav, model.sr)
    subprocess.run(["ffmpeg", "-y", "-i", "temp.wav", "temp.mp3"], check=True)
    os.remove("temp.wav")

