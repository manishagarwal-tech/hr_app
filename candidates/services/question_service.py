import json
import logging
import re
from django.conf import settings
from .llm_factory import LLMFactory
from .prompts import QUESTION_GENERATION_PROMPT

logger = logging.getLogger(__name__)


class QuestionValidator:
    def validate(self, questions):
        if not isinstance(questions, list):
            raise ValueError("Questions response must be a list.")
        for item in questions:
            if not isinstance(item, dict):
                raise ValueError("Each question must be an object.")
            if "question" not in item or "answer" not in item:
                raise ValueError("Each question must include question and answer keys.")
        return questions


class QuestionGenerationService:
    def __init__(self):
        self.validator = QuestionValidator()

    def generate(self, skill, expertise):
        llm = LLMFactory.get_chat_model(settings.QUESTION_MODEL_NAME, temperature=0)
        chain = QUESTION_GENERATION_PROMPT | llm
        response = chain.invoke({"skill": skill, "expertise": expertise})
        questions = self._parse_questions(response.content)
        return self.validator.validate(questions)

    def _parse_questions(self, content):
        cleaned = (content or "").strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)

        bracket_start = cleaned.find("[")
        bracket_end = cleaned.rfind("]")
        if bracket_start != -1 and bracket_end != -1:
            cleaned = cleaned[bracket_start: bracket_end + 1]

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            try:
                return json.loads(cleaned, strict=False)
            except json.JSONDecodeError as exc:
                logger.exception("Failed to parse question JSON. Snippet: %s", cleaned[:500])
                raise ValueError("Failed to parse questions and answers.") from exc
