from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .agents.orchestrator import ScreeningOrchestrator
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .models import CandidateProfile
from .serializers import ResumeUploadSerializer, CandidateSubmissionSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages



#  =============== LOGIN AND LOGOUT VIEWS =============== #
class PortalLoginView(View):
    template_name = 'registration/login.html'

    def get(self, request):
        if request.user.is_authenticated :
            return redirect('dashboard')
        else:
            return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('upload')  # Redirect to resume upload page on success
        else:
            messages.error(request, "Invalid username or password")
            return render(request, self.template_name)


class PortalLogoutView(View):
    """View to handle user logout and redirect to login page."""
    def get(self, request):
        logout(request)
        return redirect('login')  # Redirect to the login page

#  =============== LOGIN AND LOGOUT VIEWS =============== #

class DashboardPageView(View):
    """ first page to be display after login """
    template_name = 'candidates/dashboard.html'

    def get(self, request):
        return render(request, self.template_name)


class ResumeUploadPageView(LoginRequiredMixin, View):
    """View to render the resume upload page."""
    template_name = 'candidates/upload.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class ResumeUploadView(View):
    """API view to handle the resume upload."""

    def post(self, request, *args, **kwargs):
        resume_file = request.FILES.get('resume')

        if not resume_file:
            return JsonResponse({"error": "No resume file uploaded"}, status=400)

        # Pass data to the serializer
        serializer = ResumeUploadSerializer(data={"resume": resume_file})

        if serializer.is_valid():
            resume_file = serializer.validated_data['resume']

            if resume_file.size == 0:
                return JsonResponse({'error': 'Uploaded file is empty.'}, status=400)

            orchestrator = ScreeningOrchestrator()
            try:
                candidate, extracted_data = orchestrator.process_resume(resume_file, request.user)
            except ValueError as exc:
                return JsonResponse({"error": str(exc)}, status=400)

            # Retrieve and save top skills to session
            top_primary_skills = (candidate.primary_skills or [])[:5]
            top_secondary_skills = (candidate.secondary_skills or [])[:5]
            skills_to_display = top_primary_skills + top_secondary_skills
            request.session['skills'] = skills_to_display
            request.session['candidate_id'] = candidate.id
            return HttpResponseRedirect(reverse('display_skills'))



        return JsonResponse(serializer.errors, status=400)

    #get all submissing from the database
    def get(self, request):
        template_name = 'candidates/submission_list.html'
        candidates = CandidateProfile.objects.all()
        serializer = CandidateSubmissionSerializer(candidates, many=True)
        context = {
            "candidates": serializer.data
        }
        return render(request, template_name, context)

class GetQuestionsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        skill = request.data.get('skill')
        expertise = request.data.get('expertise')
        candidate_id = request.session.get('candidate_id')
        candidate = get_object_or_404(CandidateProfile, id=candidate_id, user=request.user)

        if not skill or not expertise:
            return JsonResponse({"error": "Skill and expertise are required."}, status=400)

        orchestrator = ScreeningOrchestrator()
        try:
            questions_list = orchestrator.generate_questions(candidate, skill, expertise)
        except ValueError as exc:
            return JsonResponse({"error": str(exc)}, status=500)

        questions_and_answers = [
            {"question": qa["question"], "answer": qa.get("answer")} for qa in questions_list
        ]
        return Response({'questions': questions_and_answers}, status=status.HTTP_200_OK)


@method_decorator(login_required, name='dispatch')
class DisplaySkillsView(View):
    """View to display extracted skills and allow expertise selection."""

    def get(self, request):
        skills = request.session.get('skills', [])
        candidate_id = request.session.get('candidate_id')

        return render(request, 'candidates/display_skills.html', {
            'skills': skills,
            'candidate_id': candidate_id,
        })


@method_decorator(login_required, name='dispatch')
class ChatRoomView(View):
    """
    View to handle the custom chat with LLM API
    """
    def get(self, request):
        template_name = 'candidates/chat.html'
        return render(request, template_name)

    def post(self, request):
        user_question = request.POST.get("chat_text", "")
        session_history = request.session.get("chat_history", [])
        orchestrator = ScreeningOrchestrator()
        candidate_id = request.session.get("candidate_id")
        profile = None
        if candidate_id:
            candidate = CandidateProfile.objects.filter(id=candidate_id, user=request.user).first()
            if candidate:
                profile = {
                    "name": candidate.name,
                    "primary_skills": candidate.primary_skills or [],
                    "secondary_skills": candidate.secondary_skills or [],
                    "experience": candidate.experience,
                }
        response = orchestrator.chat(user_question, chat_history=session_history, profile=profile)
        request.session["chat_history"] = response.get("chat_history", session_history)

        return JsonResponse({
            "human": response.get("human"),
            "ai": response.get("ai")
        })
