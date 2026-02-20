import logging
from ..models import CandidateProfile, Question

logger = logging.getLogger(__name__)


class CandidateService:
    def upsert_candidate(self, user, name, resume_file, extracted_data):
        candidate, created = CandidateProfile.objects.get_or_create(
            user=user,
            name=name,
            defaults={
                "resume": resume_file,
                "primary_skills": extracted_data.get("primary_skills", []),
                "secondary_skills": extracted_data.get("secondary_skills", []),
                "experience": extracted_data.get("experience", 0),
            },
        )

        if not created:
            candidate.resume_version += 1
            candidate.resume = resume_file
            candidate.primary_skills = extracted_data.get("primary_skills", [])
            candidate.secondary_skills = extracted_data.get("secondary_skills", [])
            candidate.experience = extracted_data.get("experience", 0)
            candidate.save()

        return candidate, created

    def store_questions(self, candidate, questions):
        for qa in questions:
            Question.objects.create(
                candidate=candidate,
                question_text=qa["question"],
                answer_text=qa.get("answer"),
            )
        return questions
