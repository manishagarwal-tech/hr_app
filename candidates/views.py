from rest_framework.views import APIView
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from .chains.groq_chain import HRChain
from django.http import JsonResponse
from .models import CandidateProfile
from .serializers import ResumeUploadSerializer
import logging
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
import fitz
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages



logger = logging.getLogger(__name__)

#  =============== LOGIN AND LOGOUT VIEWS =============== #
class PortalLoginView(View):
    template_name = 'registration/login.html'

    def get(self, request):
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

            resume_text = ""
            if isinstance(resume_file, InMemoryUploadedFile):
                pdf_data = BytesIO(resume_file.read())
                pdf_data.seek(0)

                try:
                    with fitz.open(stream=pdf_data, filetype="pdf") as pdf_document:
                        for page_num in range(pdf_document.page_count):
                            page = pdf_document[page_num]
                            resume_text += page.get_text()
                except fitz.EmptyFileError as e:
                    return JsonResponse({'error': 'The uploaded file is empty or not a valid PDF.'}, status=400)

            # Extract skills and experience
            chain = HRChain()
            extracted_data = chain.extract_skills_and_experience(resume_text)

            # Update candidate profile with extracted data
            candidate = CandidateProfile.objects.create(resume=resume_file)
            candidate.primary_skills = extracted_data.get("primary_skills", [])
            candidate.secondary_skills = extracted_data.get("secondary_skills", [])
            candidate.experience = extracted_data.get("experience", 0)
            candidate.save()

            # Retrieve top 5 primary and secondary skills
            top_primary_skills = candidate.primary_skills[:5]
            top_secondary_skills = candidate.secondary_skills[:5]
            skills_to_display = top_primary_skills + top_secondary_skills

            # Redirect to display skills page
            request.session['skills'] = skills_to_display
            request.session['candidate_id'] = candidate.id
            return redirect(reverse('display_skills'))

        return JsonResponse(serializer.errors, status=400)

class GetQuestionsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        skill = request.data.get('skill')
        expertise = request.data.get('expertise')

        # Logic to fetch questions based on the skill and expertise level
        chain = HRChain()
        questions = chain.generate_interview_questions(skill, expertise)
        return Response({'questions': questions}, status=status.HTTP_200_OK)


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