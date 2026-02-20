from .base import BaseAgent
from candidates.services.cache_service import CacheService
from candidates.services.question_service import QuestionGenerationService


class QuestionGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("question_generator")
        self.cache = CacheService()
        self.generator = QuestionGenerationService()

    def run(self, context):
        profile = context.get("profile") or {}
        profile_hash = self.cache.hash_profile(profile)
        skill = context["skill"]
        expertise = context["expertise"]

        cached_questions = self.cache.get_questions(profile_hash, skill, expertise)
        if cached_questions:
            context["questions"] = cached_questions
            return context

        questions = self.generator.generate(skill, expertise)
        self.cache.set_questions(profile_hash, skill, expertise, questions)
        context["questions"] = questions
        return context
