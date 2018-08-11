from django.urls import path
from uploads.views import *

app_name = "uploads"
urlpatterns = [
    path("", view=UploadsListAPIView.as_view()),
    path("<str:file_name>", view=UploadsListAPIView.as_view()),
]
