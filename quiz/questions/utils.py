import random

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404

from .models import QuestionCollection, Quiz


def prepare_question_set(collection: QuestionCollection) -> list:
    questions = get_list_or_404(collection.collection_questions)
    return random.sample(questions, settings.QUIZ_QUESTION_COUNT)


def prepare_quiz(
    user: User, session_key: str, collection: QuestionCollection,
) -> Quiz:
    question_choosen = prepare_question_set(collection)
    quiz, is_created = Quiz.objects.get_or_create(
        user=user, session_key=session_key, is_completed=False)
    quiz.questions.set(question_choosen, clear=True)  # type:ignore
    return quiz
