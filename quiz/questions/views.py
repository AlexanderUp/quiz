from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView

from .models import AnswerGiven, Question, QuestionType, Quiz
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
    request.session["quiz_pk"] = quiz.pk
    request.session["question_pks"] = [question.pk for question in questions]
    request.session["current_question_number"] = 0
    request.session["questions_remain"] = questions.count()
    return redirect(reverse("questions:process_question"))


def process_question(request):
    try:
        question_id = request.session["question_pks"].pop()
    except IndexError:
        return redirect("questions:quiz_result")
    else:
        request.session["current_question_number"] += 1
        request.session["questions_remain"] -= 1
        question = get_object_or_404(Question, pk=question_id)
        # possible_answers = get_possible_answers(question)
        possible_answers = question.answers.all()  # type:ignore
        context = {
            "question": question,
            "possible_answers": possible_answers,
        }
    return render(request, "questions/quiz.html", context=context)


def process_answer(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    answer_given = get_object_or_404(
        question.answers, pk=request.POST.get("choice")  # type:ignore
    )
    quiz_pk = request.session.get("quiz_pk")
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    AnswerGiven.objects.create(
        quiz=quiz, question=question, answer=answer_given)
    import sys
    print(">>>>>>>>>>>>>> answer processed", file=sys.stderr)
    return redirect(reverse("questions:process_question"))


def quiz_result(request):
    quiz = get_object_or_404(
        Quiz,
        pk=request.session.get("quiz_pk")
    )
    answers_given = quiz.answers_given.select_related(  # type:ignore
        "question", "answer")
    quiz.is_completed = True
    quiz_score = sum(
        (answer_given.answer.is_correct for answer_given in answers_given)
    )
    quiz.score = quiz_score
    quiz.save()
    context = {
        "quiz": quiz,
        "answers_given": answers_given,
    }
    return render(request, "questions/quiz_result.html", context=context)
