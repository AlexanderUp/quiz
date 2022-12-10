from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView

from .models import Question, QuestionType
from .utils import get_possible_answers, prepare_quiz


class IndexView(TemplateView):
    template_name = "questions/index.html"


def start_quiz(request):
    question_type = get_object_or_404(QuestionType, name="Math")
    quiz = prepare_quiz(
        user=request.user,
        question_type=question_type,
        session_key=request.session.session_key
    )
    questions = quiz.questions.order_by("-id").all()
    request.session["question_pks"] = [question.pk for question in questions]
    request.session["current_question_number"] = 0
    request.session["questions_remain"] = questions.count()
    return redirect(reverse("questions:process_question"))


def process_question(request):
    try:
        question_id = request.session["question_pks"].pop()
    except IndexError:
        return redirect("questions:index")
    else:
        request.session["current_question_number"] += 1
        request.session["questions_remain"] -= 1
        question = get_object_or_404(Question, pk=question_id)
        possible_answers = get_possible_answers(question)
        context = {
            "question": question,
            "possible_answers": possible_answers,
        }
    return render(request, "questions/quiz.html", context=context)
