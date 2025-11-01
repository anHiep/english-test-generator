from .question_types import choose_two_question_types
from .complex_elements import choose_complex_elements

def generate_listening_prompt(topic: str):
    types_selected = choose_two_question_types()
    complex_elements = choose_complex_elements()
    elements_text = "\n  - ".join(complex_elements)

    return f"""
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
- Each dialogue must be **long enough** to support 5 reasoning-heavy questions. Avoid short or oversimplified exchanges. The dialogues should sound natural and detailed, like a real IELTS Listening recording.
- Include realistic complex elements for challenge:
  - {elements_text}
- Ensure that there are at least 20–24 total turns combined across both dialogues, or about 3-4 minutes of spoken content.
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
- Must generate the answers for all questions.
- **Do not include any explanations, comments, or text outside the quiz content. No additional commentary or instructions. Only the formatted quiz content should appear.**
- Make sure that this quiz is in the medium difficulties (level B1 to B2). This targeted test takers for this quiz are people with intermediate English proficiency.
- Avoid very complex grammars or very hard vocabularies because this quiz is for the intermediate level.
- The targeted test takers for this quiz are around 6.5 - 7.5 in IELTS Listening proficiency.
"""
