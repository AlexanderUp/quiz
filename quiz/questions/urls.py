from django.urls import path

from . import views

app_name = "questions"

urlpatterns = (
    path("start/", views.start_quiz, name="start_quiz"),
    path(
        "question/<int:question_pk>/process_answer/",
        views.process_answer,
        name="process_answer"
    ),
    path(
        "question/", views.process_question, name="process_question"
    ),
    path(
        "quiz_result/", views.quiz_result, name="quiz_result"
    ),
    path("", views.IndexView.as_view(), name="index"),
)
