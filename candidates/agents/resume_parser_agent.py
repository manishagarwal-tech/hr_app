from .base import BaseAgent
from candidates.services.cache_service import CacheService
from candidates.services.resume_parser import ResumeParserService


class ResumeParserAgent(BaseAgent):
    def __init__(self):
        super().__init__("resume_parser")
        self.cache = CacheService()
        self.parser = ResumeParserService()

    def run(self, context):
        resume_file = context["resume_file"]
        resume_bytes = self.parser.read_bytes(resume_file)
        resume_hash = self.cache.hash_bytes(resume_bytes)
        cached_text = self.cache.get_resume_text(resume_hash)
        if cached_text:
            context["resume_text"] = cached_text
            context["resume_hash"] = resume_hash
            return context

        resume_text = self.parser.extract_text_from_bytes(resume_bytes)
        self.cache.set_resume_text(resume_hash, resume_text)
        context["resume_text"] = resume_text
        context["resume_hash"] = resume_hash
        return context
