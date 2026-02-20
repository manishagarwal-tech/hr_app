from .base import BaseAgent
from candidates.services.cache_service import CacheService
from candidates.services.extraction_service import SkillExtractionService


class SkillExtractorAgent(BaseAgent):
    def __init__(self):
        super().__init__("skill_extractor")
        self.cache = CacheService()
        self.extractor = SkillExtractionService()

    def run(self, context):
        resume_hash = context.get("resume_hash")
        cached_profile = self.cache.get_profile(resume_hash) if resume_hash else None
        if cached_profile:
            context["profile"] = cached_profile
            return context

        resume_text = context["resume_text"]
        profile = self.extractor.extract(resume_text)
        if resume_hash:
            self.cache.set_profile(resume_hash, profile)
        context["profile"] = profile
        return context
