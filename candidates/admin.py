from django.contrib import admin
from .models import CandidateProfile
# Register your models here.
admin.site.register(CandidateProfile)


def calculate_accuracy(candidate, accuracy=None):
    # Implement accuracy calculation based on predefined correct answers
    return accuracy
