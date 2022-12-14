from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView

from .models import AnswerGiven, Question, QuestionCollection, Quiz
from .utils import prepare_quiz


class IndexView(LoginRequiredMixin, ListView):
    model = QuestionCollection
    template_name = "questions/index.html"


@login_required
def start_quiz(request, collection_pk):
    collection = get_object_or_404(QuestionCollection, pk=collection_pk)
    quiz = prepare_quiz(
        user=request.user,
        session_key=request.session.session_key,
        collection=collection
    )
    questions = quiz.questions.order_by("-id").all()
    request.session["quiz_pk"] = quiz.pk
    request.session["question_pks"] = [question.pk for question in questions]
    request.session["current_question_number"] = 0
    request.session["questions_remain"] = questions.count()
    return redirect(reverse("questions:process_question"))


@login_required
def process_question(request):
    try:
        question_id = request.session["question_pks"].pop()
    except IndexError:
        return redirect("questions:quiz_result")
    else:
        request.session["current_question_id"] = question_id
        request.session["current_question_number"] += 1
        request.session["questions_remain"] -= 1
        question = get_object_or_404(Question, pk=question_id)
        possible_answers = question.answers.all()  # type:ignore
        context = {
            "question": question,
            "possible_answers": possible_answers,
        }
    return render(request, "questions/quiz.html", context=context)


@login_required
def process_answer(request, question_pk):
    answer_given_pk = request.POST.get("choice")
    if answer_given_pk is None:
        request.session["current_question_number"] -= 1
        request.session["questions_remain"] += 1
        request.session["question_pks"].append(
            request.session["current_question_id"])
        return redirect(reverse("questions:process_question"))

    question = get_object_or_404(Question, pk=question_pk)
    answer_given = get_object_or_404(
        question.answers, pk=answer_given_pk  # type:ignore
    )
    quiz = get_object_or_404(Quiz, pk=request.session.get("quiz_pk"))
    AnswerGiven.objects.create(
        quiz=quiz, question=question, answer=answer_given)
    return redirect(reverse("questions:process_question"))


@login_required
def quiz_result(request):
    quiz = Quiz.objects.prefetch_related("questions").get(
        pk=request.session.get("quiz_pk")
    )
    answers_given = quiz.answers_given.select_related(  # type:ignore
        "question", "answer").order_by("id")
    quiz.is_completed = True
    quiz_score = sum(
        (answer_given.answer.is_correct for answer_given in answers_given)
    )
    quiz.score = quiz_score
    quiz.save()
    context = {
        "answers_given": answers_given,
        "quiz": quiz,
        "wrong_answers_count": quiz.questions.count() - quiz.score,
        "percentage": round(quiz.score / quiz.questions.count() * 100, 2),
    }
    return render(request, "questions/quiz_result.html", context=context)
