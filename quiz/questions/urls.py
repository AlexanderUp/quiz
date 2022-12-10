from django.urls import path

from . import views

app_name = "questions"

urlpatterns = (
    path("start/", views.start_quiz, name="start_quiz"),
    path(
        "question/", views.process_question, name="process_question"
    ),
    path("", views.IndexView.as_view(), name="index"),
)
