from django.db import models

class CandidateProfile(models.Model):
    name = models.CharField(max_length=100)
    primary_skills = models.JSONField(null=True, blank=True)
    secondary_skills = models.JSONField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    resume = models.FileField(upload_to='resumes/')
    expertise_level = models.CharField(max_length=10, choices=[('Beginner', 'Beginner'), ('Medium', 'Medium'), ('Expert', 'Expert')])
    answers = models.JSONField(null=True, blank=True)  # To store answers
    created_at = models.DateTimeField(auto_now_add=True)
