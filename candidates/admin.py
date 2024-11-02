from django.contrib import admin
from .models import CandidateProfile, Question

# Register your models here.
admin.site.register(CandidateProfile)
admin.site.register(Question)
