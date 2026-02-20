from .resume_parser_agent import ResumeParserAgent
from .skill_extractor_agent import SkillExtractorAgent
from .question_generator_agent import QuestionGeneratorAgent
from .validator_agent import ValidatorAgent
from .chat_agent import ChatAgent
from candidates.services.candidate_service import CandidateService


class ScreeningOrchestrator:
    def __init__(self):
        self.resume_parser = ResumeParserAgent()
        self.skill_extractor = SkillExtractorAgent()
        self.question_generator = QuestionGeneratorAgent()
        self.validator = ValidatorAgent()
        self.chat_agent = ChatAgent()
        self.candidate_service = CandidateService()

    def process_resume(self, resume_file, user):
        context = {"resume_file": resume_file}
        context = self.resume_parser.run(context)
        context = self.skill_extractor.run(context)

        profile = context["profile"]
        candidate_name = profile.get("name", "Unknown")
        candidate, _created = self.candidate_service.upsert_candidate(
            user=user,
            name=candidate_name,
            resume_file=resume_file,
            extracted_data=profile,
        )

        return candidate, profile

    def generate_questions(self, candidate, skill, expertise, profile=None):
        context = {
            "profile": profile or self._profile_from_candidate(candidate),
            "skill": skill,
            "expertise": expertise,
        }
        context = self.question_generator.run(context)
        context = self.validator.run(context)
        questions = context["questions"]
        self.candidate_service.store_questions(candidate, questions)
        return questions

    def chat(self, user_question, chat_history=None, profile=None):
        context = {
            "user_question": user_question,
            "chat_history": chat_history or [],
            "profile": profile,
        }
        context = self.chat_agent.run(context)
        return context["chat_response"]

    def _profile_from_candidate(self, candidate):
        return {
            "name": candidate.name,
            "primary_skills": candidate.primary_skills or [],
            "secondary_skills": candidate.secondary_skills or [],
            "experience": candidate.experience,
        }
