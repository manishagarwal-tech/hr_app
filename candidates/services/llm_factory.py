import logging
from django.conf import settings
from langchain_groq import ChatGroq

logger = logging.getLogger(__name__)


class LLMFactory:
    _instances = {}

    @classmethod
    def get_chat_model(cls, model_name, temperature=0):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not configured.")
        key = (model_name, temperature)
        if key not in cls._instances:
            cls._instances[key] = ChatGroq(
                temperature=temperature,
                groq_api_key=settings.GROQ_API_KEY,
                model_name=model_name,
            )
            logger.info("Initialized Groq model: %s", model_name)
        return cls._instances[key]
