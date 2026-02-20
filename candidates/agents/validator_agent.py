from .base import BaseAgent
from candidates.services.question_service import QuestionValidator


class ValidatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("validator")
        self.validator = QuestionValidator()

    def run(self, context):
        questions = context.get("questions", [])
        self.validator.validate(questions)
        return context
