import random

QUESTION_TYPES = [
    {
        "name": "Sentence Completion",
        "description": (
            "Candidates must fill in missing words or numbers in sentences. "
            "Each question contains a sentence with a gap made of underscores. "
            "The answer will be a word or phrase that fills that gap. Example:\n"
            "1. Tim wants _____ bananas.\n"
            "* five\n* 5\n"
            "Include elements that require reasoning from multiple pieces of information "
            "or corrections by speakers."
        )
    },
    {
        "name": "Short Answer Questions",
        "description": (
            "Candidates must provide short answers based on the audio. "
            "Many details may be extra, misleading, or require logical inference. "
            "Include elements such as decision-making, time adjustments, or partially corrected information."
        )
    }
]

def choose_two_question_types():
    return random.sample(QUESTION_TYPES, 2)
