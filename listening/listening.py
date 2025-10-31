from handler.llm import call_llm
import random

# -----------------------------
# Step 1: Define question types
# -----------------------------
QUESTION_TYPES = [
    # {
    #     "name": "Multiple Choice Questions",
    #     "description": "Candidates must select one answer from three options, which may include distractors. Some information may be implied and require reasoning. Include elements where candidates must infer answers or detect contradictions."
    # },
    {
        "name": "Sentence Completion",
        "description": "Candidates must fill in missing words or numbers in sentences. Each question contains a sentence with a gap made of underscores. The answer will be a word or phrase that fills that gap. Example:\n1. Tim wants _____ bananas.\n* five\n* 5\nInclude elements that require reasoning from multiple pieces of information or corrections by speakers."
    },
    {
        "name": "Short Answer Questions",
        "description": "Candidates must provide short answers based on the audio. Many details may be extra, misleading, or require logical inference. Include elements such as decision-making, time adjustments, or partially corrected information."
    }
]

# -----------------------------
# Step 2: Randomly select 2 different types
# -----------------------------
def choose_two_question_types():
    return random.sample(QUESTION_TYPES, 2)

# -----------------------------
# Step 3: Define possible dialogue topics
# -----------------------------
DIALOGUE_TOPICS = [
    # Accommodation & Housing
    "Booking a hotel room",
    "Renting an apartment",
    "Renewing a rental contract",
    "Reporting a broken appliance to a landlord",
    "Booking a hostel bed",
    "Arranging student accommodation",
    "Discussing moving services",
    "Paying a utility bill",
    "Requesting a home inspection",
    "Inquiring about furniture delivery",

    # Travel & Transport
    "Arranging airport transport",
    "Buying a train ticket",
    "Booking a guided city tour",
    "Rescheduling a flight",
    "Reporting lost luggage",
    "Buying travel insurance",
    "Renting a car",
    "Checking into a cruise trip",
    "Asking about a bus schedule",
    "Booking a taxi service",

    # Education & Courses
    "Enrolling in a language course",
    "Registering for evening classes",
    "Asking about university accommodation",
    "Discussing tuition fees",
    "Booking a campus tour",
    "Applying for a scholarship",
    "Scheduling a placement test",
    "Arranging private tutoring",
    "Inquiring about online courses",
    "Asking for a course refund",

    # Health & Wellness
    "Scheduling a doctor appointment",
    "Consulting a dentist about treatment",
    "Registering at a health clinic",
    "Booking a physiotherapy session",
    "Inquiring about a vaccination",
    "Asking about medical insurance coverage",
    "Joining a fitness class",
    "Applying for a gym membership",
    "Booking a nutrition consultation",
    "Arranging home nursing services",

    # Daily Services & Errands
    "Requesting house cleaning service",
    "Ordering office supplies",
    "Getting a pet groomed",
    "Booking laundry pickup",
    "Reporting a maintenance issue",
    "Renewing a phone contract",
    "Setting up a bank account",
    "Applying for a library card",
    "Ordering catering for an event",
    "Booking photography services",

    # Leisure & Events
    "Buying tickets for a concert",
    "Making a restaurant reservation",
    "Booking a conference venue",
    "Planning a holiday package",
    "Registering for a marathon",
    "Joining a community workshop",
    "Booking tickets for a theatre show",
    "Arranging a picnic event",
    "Reserving a camping site",
    "Planning a birthday party",

    # Shopping & Customer Support
    "Returning a defective product",
    "Asking about refund policies",
    "Inquiring about store membership discounts",
    "Placing an online order",
    "Tracking a package delivery",
    "Reporting a lost item",
    "Checking product availability",
    "Exchanging a purchased item",
    "Requesting a price quote",
    "Complaining about poor service"
]

def choose_dialogue_topic():
    return random.choice(DIALOGUE_TOPICS)

# -----------------------------
# Step 4: Define complex elements
# -----------------------------
COMPLEX_ELEMENTS = [
    # Common factual but error-prone details
    "Names spelled out letter by letter (e.g., 'That’s S-M-I-T-H')",
    "Addresses combining house number + street + area (e.g., '19 Stone Avenue, Eastlake')",
    "Postcodes mixing letters and numbers",
    "Phone numbers with pauses or corrections",
    "Dates mentioned in different formats or corrected (e.g., 'the 13th — oh sorry, the 30th')",

    # Transaction and booking details
    "Payment method mentioned among options (cash / credit card / cheque)",
    "Service or booking details corrected or updated mid-dialogue (time, location, or item)",

    # Reasoning and inference elements
    "Information corrected or contradicted by another speaker (requiring logical reconciliation)",
    "Multiple options given, only one chosen (decision logic)",
    "Extra or irrelevant information acting as distractors (not part of the answer)",
    "Details spread across multiple sentences that must be connected for one answer",

    # Realistic traps
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

# -----------------------------
# Step 5: Generate LLM prompt
# -----------------------------
def generate_listening_part1_prompt():
    types_selected = choose_two_question_types()
    topic = choose_dialogue_topic()
    complex_elements = choose_complex_elements()
    elements_text = "\n  - ".join(complex_elements)

    prompt = f"""
You are to generate a **difficult IELTS Listening Part 1 test** with exactly 10 questions, arranged as **2 separate dialogues** that form a **continuous scenario**.

1. QUESTION TYPES:
- Include exactly 2 types randomly selected from: {types_selected[0]['name']} and {types_selected[1]['name']}.
- Each type is applied to one dialogue: first dialogue uses the first type, second dialogue uses the second type.
- **Both dialogues share the same topic, characters, and setting. Dialogue 2 is a direct continuation of Dialogue 1, continuing the same conversation with new information or developments.**
- **Questions from the first section must rely only on information in the first dialogue. Questions from the second section must rely only on information in the second dialogue.**
- Question type descriptions in English:
  - Multiple Choice Questions: Candidates must select one answer from three options, which may include distractors. Some information may be implied and require reasoning. Include elements where candidates must infer answers or detect contradictions.
  - Sentence Completion (Gap-Filling): Candidates must fill in missing words or numbers in sentences. Each question contains a sentence with a gap made of underscores. The answer will be a word or phrase that fills that gap. Example:
1. Tim wants _____ bananas.
* five
* 5
Include elements that require reasoning from multiple pieces of information or corrections by speakers.
  - Short Answer Questions: Candidates must provide short answers based on the audio. Many details may be extra, misleading, or require logical inference. Include elements such as decision-making, time adjustments, or partially corrected information.

2. DIALOGUES:
- Shared Topic: {topic}
- Dialogue 1 and Dialogue 2 both take place within this same scenario and feature the same characters. The second dialogue must begin naturally from the first (e.g., following up a booking, continuing a call, clarifying details, or confirming arrangements).
- Each dialogue must be **long enough** to support 5 reasoning-heavy questions (at least 18–24 total turns combined). Avoid short or oversimplified exchanges. The dialogues should sound natural and detailed, like a real IELTS Listening recording.
- Include realistic complex elements for challenge:
  - {elements_text}
- Ensure that **100% of questions involve logical or inferential reasoning**: combining information across lines, interpreting corrections, choosing between distractors, or inferring time/number changes.

3. TEXT2QTI SYNTAX AND TEXT: BLOCK RULES:
- All dialogue, instructions, and general info must be inside Text: blocks.
- All task instructions (e.g., “Answer the questions below.”, “Write NO MORE THAN TWO WORDS AND/OR A NUMBER…”) must also appear inside a Text: block, following the same indentation rules. For example:
Text: Instructions: Answer the questions below.
      Write **NO MORE THAN TWO WORDS AND/OR A NUMBER** for each answer.
- Alignment rules:
  - First line of Text: block: 0 spaces
  - Dialogue paragraphs after first line: 6 spaces
  - General info / instructions paragraphs after first line (including sentence-completion gaps): 6 spaces
  - Tables and images: always 4 spaces
- Indentation Reinforcement (MANDATORY):
  - The 'Text:' label itself starts at the beginning of the line (no leading spaces).
  - Every line inside the Text: block must follow these exact indentation rules:
      * The first paragraph starts with exactly 6 spaces.
      * Every subsequent paragraph also starts with exactly 6 spaces and is separated from the previous one by a blank line.
      * Tables and images inside Text: blocks must always be indented with exactly 4 spaces, regardless of position.
  - These spacing rules are strict and must be consistent throughout the entire output.
- Examples:
    Dialogue (always 6 spaces):
Text: You will hear Bob and Mary talking about an upcoming booking

      Bob: Hi Mary, how have you been preparing for the tests?

      Mary: It's coming along Bob, how about you?

      Bob: I haven't had time mate.

  Table (always 4 spaces):
Text: Maximum students per course
    <table border="1" cellpadding="4" cellspacing="0">
      <tr>
        <th>Course</th>
        <th>Max Students</th>
      </tr>
      <tr>
        <td>Introduction to Biology</td>
        <td>50</td>
      </tr>
      <tr>
        <td>Advanced Mathematics</td>
        <td>40</td>
      </tr>
    </table>

  Image (always 4 spaces):
Text: Campus map
    ![Campus map](img1.png)
    
4. QUESTION FORMATTING:
- Two separate dialogues, each followed by 5 questions
- Dialogue 2 continues the scenario of Dialogue 1 directly
- Questions numbered sequentially from 1 to 10 across both dialogues
- Multi-paragraph problem statements: first line 0 spaces, subsequent paragraphs 3 spaces
- Multiple choice answers: start at beginning of line, correct answer preceded by '*'
- Short answer / sentence completion answers: start at beginning of line, each correct answer preceded by '*'
- Sentence completion questions **must include a correct answer**
- **When a question asks about an amount of money, the currency symbol (£, $, etc.) must appear in the question text, NOT in the answer. Example:**  
  - Correct: “The price of the adult ticket was £___?”  
    * 300  
  - Incorrect: “The price of the adult ticket was ____?”  
    * £300
- Example for multiple choice:
1. What does Bob ask first?
a) About exam results
*b) How Mary prepared for the test
c) About tuition fees

- Example for short answer / sentence completion:
5. The customer is booking the room for ___ people.
* 2

- Every question must involve reasoning or inference — for example, combining clues, identifying contradictions, or deducing implied meanings.

5. OUTPUT INSTRUCTIONS:
- Only output quiz content strictly following text2qti formatting rules
- Dialogue, instructions, tables, images, and general info (including sentence completion gaps) must be inside Text: blocks
- Maintain exact indentation rules for all paragraphs
- Questions must be integrated naturally with dialogues
- Number questions sequentially from 1 to 10
- For Short Answer and Sentence Completion (gap filling) questions, there must be a space between the * symbol and the answer.
- **Do not include any explanations, comments, or text outside the quiz content. No additional commentary or instructions. Only the formatted quiz content should appear.**
"""
    return prompt

# -----------------------------
# Step 6: Call LLM
# -----------------------------
def generate_listening_part1():
    prompt = generate_listening_part1_prompt()
    sample_prompt = [
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "assistant", "content": "Hello! How can I assist you today?"},
        {"role": "user", "content": prompt}
    ]
    response = call_llm(messages=sample_prompt, model="google/gemini-2.5-pro")
    return response