from django.db import models
from django.contrib.auth.models import User

class CandidateProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="candidates")
    name = models.CharField(max_length=100)
    primary_skills = models.JSONField(null=True, blank=True)
    secondary_skills = models.JSONField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    resume = models.FileField(upload_to='resumes/')
    created_at = models.DateTimeField(auto_now_add=True)
    resume_version = models.IntegerField(default=1)

class Question(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    answer_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)