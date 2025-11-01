import random

COMPLEX_ELEMENTS = [
    "Names spelled out letter by letter (e.g., 'That’s S-M-I-T-H')",
    "Addresses combining house number + street + area (e.g., '19 Stone Avenue, Eastlake')",
    "Postcodes mixing letters and numbers",
    "Phone numbers with pauses or corrections",
    "Dates mentioned in different formats or corrected (e.g., 'the 13th — oh sorry, the 30th')",
    "Payment method mentioned among options (cash / credit card / cheque)",
    "Service or booking details corrected or updated mid-dialogue (time, location, or item)",
    "Information corrected or contradicted by another speaker (requiring logical reconciliation)",
    "Multiple options given, only one chosen (decision logic)",
    "Extra or irrelevant information acting as distractors (not part of the answer)",
    "Details spread across multiple sentences that must be connected for one answer",
    "Similar-sounding words or numbers used as distractors",
    "Indirect answers (e.g., 'She’ll arrive an hour earlier than planned' means 6:00 instead of 7:00)"
]

def choose_complex_elements():
    always_include = [
        "Logical inference: connecting multiple pieces of info, detecting contradictions",
        "Amounts or times requiring calculation or logic (e.g., discount, total cost, time changes)",
        "Corrections made by speakers (e.g., changing a date, number, or detail)",
        "Distractors: extra or misleading details that are not part of the answer",
        "Decision-making elements (e.g., choosing between options)"
    ]
    optional_elements = random.sample(
        [e for e in COMPLEX_ELEMENTS if e not in always_include],
        k=random.randint(3, 5)
    )
    return always_include + optional_elements + [
        "Note: The always_include elements above must appear multiple times throughout both dialogues."
    ]
