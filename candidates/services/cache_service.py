import hashlib
import json
from django.conf import settings
from django.core.cache import cache


class CacheService:
    namespace = "candidates"

    @staticmethod
    def _hash_bytes(value):
        return hashlib.sha256(value).hexdigest()

    @staticmethod
    def _hash_json(value):
        raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def resume_text_key(self, resume_hash):
        return f"{self.namespace}:resume_text:{settings.CACHE_VERSION}:{resume_hash}"

    def profile_key(self, resume_hash):
        return f"{self.namespace}:profile:{settings.CACHE_VERSION}:{resume_hash}"

    def questions_key(self, profile_hash, skill, expertise):
        composite = f"{profile_hash}|{skill}|{expertise}|{settings.PROMPT_VERSION}"
        key_hash = self._hash_bytes(composite.encode("utf-8"))
        return f"{self.namespace}:questions:{settings.CACHE_VERSION}:{key_hash}"

    def get_resume_text(self, resume_hash):
        return cache.get(self.resume_text_key(resume_hash))

    def set_resume_text(self, resume_hash, text):
        cache.set(self.resume_text_key(resume_hash), text, settings.CACHE_TTLS["resume_text"])

    def get_profile(self, resume_hash):
        return cache.get(self.profile_key(resume_hash))

    def set_profile(self, resume_hash, profile):
        cache.set(self.profile_key(resume_hash), profile, settings.CACHE_TTLS["profile"])

    def get_questions(self, profile_hash, skill, expertise):
        return cache.get(self.questions_key(profile_hash, skill, expertise))

    def set_questions(self, profile_hash, skill, expertise, questions):
        cache.set(
            self.questions_key(profile_hash, skill, expertise),
            questions,
            settings.CACHE_TTLS["questions"],
        )

    def hash_profile(self, profile):
        return self._hash_json(profile)

    def hash_bytes(self, value):
        return self._hash_bytes(value)
