from django.urls import path
from django.conf.urls.static import static

from hr_app import settings
from .views import (
        ResumeUploadPageView,
        DashboardPageView,
        ResumeUploadView,
        DisplaySkillsView,
        GetQuestionsView,
        ChatRoomView
    )

urlpatterns = [
    path('dashboard/', DashboardPageView.as_view(), name='dashboard'),
    path('upload/', ResumeUploadPageView.as_view(), name='upload'),
    path('upload_resume/', ResumeUploadView.as_view(), name='upload_resume'),
    path('get_questions/', GetQuestionsView.as_view(), name='get_questions'),
    path('display_skills/', DisplaySkillsView.as_view(), name='display_skills'),
    path('submissions/', ResumeUploadView.as_view(), name='submissions'),
    path('chat/', ChatRoomView.as_view(), name='chat')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)