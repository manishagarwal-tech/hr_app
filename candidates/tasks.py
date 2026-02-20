from celery import shared_task
from .agents.orchestrator import ScreeningOrchestrator
from .models import CandidateProfile


@shared_task
def generate_questions_task(candidate_id, skill, expertise):
    candidate = CandidateProfile.objects.get(id=candidate_id)
    orchestrator = ScreeningOrchestrator()
    questions = orchestrator.generate_questions(candidate, skill, expertise)
    return {
        "candidate_id": candidate_id,
        "question_count": len(questions),
    }
