from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

RESUME_EXTRACTION_PROMPT = PromptTemplate.from_template(
    """
### RESUME TEXT:
{resume_text}
### INSTRUCTION:
Extract the candidate's name, primary skills, secondary skills, and experience level in years from the resume text.
Return JSON with keys: name, primary_skills, secondary_skills, experience.
### VALID JSON:
"""
)

QUESTION_GENERATION_PROMPT = PromptTemplate.from_template(
    """
### ROLE
You are a senior interviewer conducting a 1:1 technical interview.

### TASK
Generate exactly 5 interview questions and model answers based on the given skill and expertise level.
Questions must feel like real 1:1 interview questions for this skill at the stated level.

Skill: {skill}
Expertise Level: {expertise}

### REQUIREMENTS
- At least 2 questions must be coding questions that require writing code or queries.
- The remaining questions should be conceptual, scenario-based, or experience-focused.
- Avoid generic questions; each should be specific and test real-world understanding.
- Align depth to expertise level:
  - Beginner: fundamentals, basic usage, simple scenarios.
  - Intermediate: trade-offs, debugging, practical design decisions, moderate complexity.
  - Expert: edge cases, performance, system constraints, architectural trade-offs.

### OUTPUT FORMAT
Respond with a JSON array of exactly 5 objects. Each object must include:
- question
- answer
- question_type (one of: "coding", "conceptual", "scenario")
- difficulty (one of: "beginner", "intermediate", "expert")

### RULES
- No extra text outside JSON.
- Do not reference tools or technologies not implied by the skill.
- Ensure at least 2 items have question_type = "coding".
- Escape any newlines inside strings as \\n.

### VALID JSON:
"""
)

CHAT_SYSTEM_PROMPT = (
    "You are a knowledgeable and helpful AI assistant. "
    "Provide clear, direct, and concise answers. "
    "Avoid unnecessary details or lengthy explanations. "
    "Respond in 2-4 sentences maximum unless the user explicitly asks for more detail. "
    "If the user asks a question related to code generation, format your response inside Markdown-style code blocks."
)


def build_chat_prompt():
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("{system_prompt}"),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{human_input}"),
    ])
