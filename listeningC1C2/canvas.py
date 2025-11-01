from canvasapi import Canvas
from dotenv import load_dotenv
import zipfile
import os
import requests
import json
from time import sleep
from termcolor import colored

load_dotenv()

API_URL = os.getenv("CANVAS_LMS_API_URL")
API_KEY = os.getenv("CANVAS_LMS_API_KEY")
COURSE_ID = os.getenv("COURSE_ID")


def insert_mp3(topic: str, num_quiz: int):
    resource_id = f"media_quiz{num_quiz}"
    html_code = (
        '&lt;p&gt;&lt;audio style="width: 320px; height: 14.25rem; display: inline-block;" '
        'title="Audio player for audio.mp3" data-media-type="audio" loading="lazy" '
        'data-media-id="maybe"&gt;&lt;source src="media/audio.mp3?canvas_=1&amp;amp;canvas_qs_embedded=true&amp;amp;canvas_qs_amp%3Btype=audio" '
        'data-media-id="maybe" data-media-type="audio"&gt;&lt;/audio&gt;&lt;/p&gt;'
    )

    resource_xml = (
        f'<resource identifier="{resource_id}" type="webcontent" href="media/audio.mp3">\n'
        f'  <file href="media/audio.mp3"/>\n'
        f'</resource>\n'
    )

    original_zip_path = "qti.zip"
    new_zip_path = "qti_audio.zip"

    print(colored("[RUNNING]", "blue"), "Injecting audio player into QTI package...")

    with zipfile.ZipFile(original_zip_path, "r") as zip_read:
        zip_contents = {name: zip_read.read(name) for name in zip_read.namelist()}

        xml_filename = next(
            (name for name in zip_contents if name.startswith("text2qti_assessment") and name.endswith("assessment_meta.xml")),
            None,
        )
        if not xml_filename:
            print(colored("[ERROR]", "red"), "No assessment_meta.xml found.")
            return
        print(colored("[FOUND]", "cyan"), f"Assessment XML file: {colored(xml_filename, 'yellow')}")

        xml_text = zip_contents[xml_filename].decode("utf-8")
        lines = xml_text.splitlines()
        if len(lines) > 3:
            lines[3] = lines[3][:15] + html_code + lines[3][15:]
        modified_xml_text = "\n".join(lines)
        zip_contents[xml_filename] = modified_xml_text.encode("utf-8")
        print(colored("[MODIFY]", "cyan"), f"Inserted audio HTML into {colored(xml_filename, 'yellow')}")

        manifest_filename = next((name for name in zip_contents if name.endswith("imsmanifest.xml")), None)
        if not manifest_filename:
            print(colored("[ERROR]", "red"), "No imsmanifest.xml found.")
            return
        print(colored("[FOUND]", "cyan"), f"Manifest file: {colored(manifest_filename, 'yellow')}")

        manifest_text = zip_contents[manifest_filename].decode("utf-8")
        if "</resources>" in manifest_text:
            manifest_text = manifest_text.replace("</resources>", resource_xml + "</resources>")
            zip_contents[manifest_filename] = manifest_text.encode("utf-8")
            print(colored("[MODIFY]", "cyan"), "Added media resource to manifest.")
        else:
            print(colored("[ERROR]", "red"), "No </resources> tag found in manifest.")

    with zipfile.ZipFile(new_zip_path, "w") as zip_write:
        for name, data in zip_contents.items():
            zip_write.writestr(name, data)

    print(colored("[DONE]", "green"), "Modified ZIP saved as:", colored(new_zip_path, "yellow"))


def upload_qti_to_canvas(file_path: str, module):
    print(colored("[RUNNING]", "blue"), "Starting QTI upload to Canvas...")

    payload = {
        "migration_type": "qti_converter",
        "pre_attachment": {"name": "qti.zip"},
        "settings": {"import_quizzes_next": False},
    }
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    response = requests.post(
        f"{API_URL}/api/v1/courses/{COURSE_ID}/content_migrations/",
        headers=headers,
        data=json.dumps(payload),
    )
    response.raise_for_status()

    migration = response.json()
    migration_id = migration["id"]
    upload_url = migration["pre_attachment"]["upload_url"]
    upload_params = migration["pre_attachment"]["upload_params"]

    print(colored("[UPLOAD]", "magenta"), f"Uploading QTI file: {colored(file_path, 'yellow')}")
    with open(file_path, "rb") as file:
        files = {"file": (upload_params["Filename"], file)}
        upload_response = requests.post(upload_url, data=upload_params, files=files)
        upload_response.raise_for_status()
    print(colored("[DONE]", "green"), "Upload completed. Waiting for migration...")

    progress_url = migration["progress_url"]
    while True:
        progress_response = requests.get(progress_url, headers=headers)
        progress_response.raise_for_status()
        progress = progress_response.json()
        completion = progress.get("completion", 0)
        print(f"\rMigration progress: {completion}% complete", end="\n")
        if progress["workflow_state"] == "completed":
            print(colored("[SUCCESS]", "green"), "Migration completed successfully.")
            break
        elif progress["workflow_state"] == "failed":
            print(colored("[ERROR]", "red"), "Migration failed.")
            return None
        sleep(3)

    canvas = Canvas(API_URL, API_KEY)
    course = canvas.get_course(COURSE_ID)
    quizzes = list(course.get_quizzes())
    new_quiz = max(quizzes, key=lambda q: q.id, default=None)

    if not new_quiz:
        print(colored("[ERROR]", "red"), "No new quiz created.")
        return None

    new_quiz.edit(quiz={"published": True})
    print(colored("[DONE]", "green"), f"Quiz '{colored(new_quiz.title, 'yellow')}' published.")

    existing_items = list(module.get_module_items())
    if any(item.title == new_quiz.title for item in existing_items):
        print(colored("[INFO]", "cyan"), f"Quiz '{new_quiz.title}' already exists in module '{module.name}'.")
    else:
        module.create_module_item({
            "type": "Quiz",
            "content_id": new_quiz.id,
            "title": new_quiz.title,
            "published": True,
        })
        print(colored("[ADD]", "cyan"), f"Added quiz '{new_quiz.title}' to module '{module.name}'.")

    quiz_url = f"{API_URL}/courses/{COURSE_ID}/quizzes/{new_quiz.id}"
    print(colored("[SUCCESS]", "green"), "Quiz available at:", colored(quiz_url, "yellow"))
    return quiz_url