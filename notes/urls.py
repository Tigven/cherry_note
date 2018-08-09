from django.urls import path

from notes.views import *

app_name = "notes"
urlpatterns = [
    path("", view=NotesListAPIView.as_view(), name="list"),
]