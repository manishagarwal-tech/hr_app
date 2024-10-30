from django.urls import path
from .views import (
        ResumeUploadPageView,
        DashboardPageView,
        ResumeUploadView,
        DisplaySkillsView,
        GetQuestionsView
    )

urlpatterns = [
    path('dashboard/', DashboardPageView.as_view(), name='dashboard'),
    path('upload/', ResumeUploadPageView.as_view(), name='upload'),
    path('upload_resume/', ResumeUploadView.as_view(), name='upload_resume'),
    path('get_questions/', GetQuestionsView.as_view(), name='get_questions'),
    path('display_skills/', DisplaySkillsView.as_view(), name='display_skills'),

]