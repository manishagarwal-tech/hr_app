import logging
from django.conf import settings
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from .llm_factory import LLMFactory
from .prompts import RESUME_EXTRACTION_PROMPT

logger = logging.getLogger(__name__)


class SkillExtractionService:
    def extract(self, resume_text):
        llm = LLMFactory.get_chat_model(settings.LLM_MODEL_NAME, temperature=0)
        chain = RESUME_EXTRACTION_PROMPT | llm
        response = chain.invoke({"resume_text": resume_text})
        try:
            json_parser = JsonOutputParser()
            extracted_data = json_parser.parse(response.content)
        except OutputParserException as exc:
            logger.exception("Failed to parse extraction output")
            raise ValueError("Error parsing skills and experience.") from exc
        return extracted_data
