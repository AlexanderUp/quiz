import random

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404

from .models import Question, QuestionType, Quiz


def prepare_quiz(
    user: User, question_type: QuestionType, session_key: str
) -> Quiz:
    questions = get_list_or_404(question_type.questions)  # type:ignore
    question_choosen = random.sample(questions, settings.QUIZ_QUESTION_COUNT)
    quiz, is_created = Quiz.objects.get_or_create(
        user=user, session_key=session_key, is_completed=False)
    quiz.questions.set(question_choosen, clear=True)  # type:ignore
    return quiz


def get_possible_answers(question: Question):
    possible_answers = get_list_or_404(question.answers)  # type:ignore
    return random.sample(
        possible_answers, settings.POSSIBLE_ANSWER_COUNT
    )
