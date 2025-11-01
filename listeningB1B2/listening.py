from termcolor import colored
import os
import zipfile
import shutil
from time import sleep

from .qti import generate_qti
from .canvas import insert_mp3, upload_qti_to_canvas
from .generator import generate_listening


def create_listening_quiz(content: str, quiz_idx: int, dist_path: str, topic: str, module):
    raw_test_dir = os.path.join(dist_path, "listening", f"{quiz_idx}")
    os.makedirs(raw_test_dir, exist_ok=True)

    print(colored("[RUNNING]", "blue"), f"Generating Listening Part 1 for idea {quiz_idx+1}: {content}")
    listening, prompt = generate_listening(content)
    print(colored("[DONE]", "green"), f"Generated Listening Part 1 for idea {quiz_idx+1}")

    # Write listening part
    raw_test_path = os.path.join(raw_test_dir, "raw_test.txt")
    with open(raw_test_path, "w", encoding="utf-8") as f:
        f.write(listening)
    print(colored("[WRITE]", "cyan"), "Saved listening part to:", colored(raw_test_path, "yellow"))

    # Write prompt
    prompt_path = os.path.join(raw_test_dir, "prompt.txt")
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(prompt)
    print(colored("[WRITE]", "cyan"), "Saved prompt to:", colored(prompt_path, "yellow"))

    # Generate QTI
    print(colored("[RUNNING]", "blue"), "Generating QTI package...")
    generate_qti(listening, quiz_idx, topic)
    print(colored("[DONE]", "green"), "QTI package created.")

    # Insert MP3
    print(colored("[RUNNING]", "blue"), "Inserting MP3 audio file...")
    insert_mp3(1, quiz_idx)
    print(colored("[DONE]", "green"), "Inserted MP3 audio file.")

    # Extract QTI zip and insert audio
    extract_dir = "qti_extracted"
    print(colored("[RUNNING]", "blue"), "Extracting QTI audio package...")
    with zipfile.ZipFile("qti_audio.zip", "r") as zip_ref:
        zip_ref.extractall(extract_dir)
    print(colored("[DONE]", "green"), "Extracted QTI audio package.")

    target_folder = os.path.join(extract_dir, "media")
    os.makedirs(target_folder, exist_ok=True)

    print(colored("[COPY]", "cyan"), "Adding audio.mp3 to media folder...")
    shutil.copy("audio.mp3", os.path.join(target_folder, "audio.mp3"))

    # Rezip into final QTI package
    final_zip_path = "final_qti.zip"
    print(colored("[RUNNING]", "blue"), "Creating final QTI zip with audio...")
    with zipfile.ZipFile(final_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(extract_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, extract_dir)
                zipf.write(abs_path, rel_path)
    print(colored("[DONE]", "green"), f"Created {colored(final_zip_path, 'yellow')}")

    # Upload to Canvas
    print(colored("[UPLOAD]", "magenta"), "Uploading QTI to Canvas...")
    quiz_url = upload_qti_to_canvas(final_zip_path, module)

    # Save outputs
    for file in ["qti.zip", "qti.txt", "audio.mp3"]:
        if os.path.exists(file):
            shutil.copy(file, os.path.join(raw_test_dir, file))
            os.remove(file)
            print(colored("[SAVE]", "cyan"), f"Stored {file} in:", colored(raw_test_dir, "yellow"))

    # Cleanup
    for temp_item in ["qti_extracted", "qti_audio.zip", "final_qti.zip"]:
        if os.path.exists(temp_item):
            if os.path.isdir(temp_item):
                shutil.rmtree(temp_item)
            else:
                os.remove(temp_item)
            print(colored("[CLEAN]", "red"), f"Removed temporary {temp_item}")

    sleep(2)

    if quiz_url:
        print(colored("[SUCCESS]", "green"), f"Quiz available at: {colored(quiz_url, 'yellow')}")
    else:
        print(colored("[ERROR]", "red"), "Failed to upload quiz to Canvas.")

    print(colored("[DONE]", "green"), "Listening quiz generation complete.")