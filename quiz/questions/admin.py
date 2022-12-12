from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import (Answer, AnswerGiven, Question, QuestionCollection,
                     QuestionType, Quiz)


class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "question",
        "question_type",
        "question_description",
        "description",
        "is_correct",
    )
    list_select_related = (
        "question",
        "question__question_type",
    )
    empty_value = "-- empty --"


class AnswerAdminFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()
        answer_correctness = (
            form.cleaned_data["is_correct"] for form in self.forms
            if form.cleaned_data
        )
        validness = any(answer_correctness) and not all(answer_correctness)
        if not validness:
            raise ValidationError(
                "Answer set is incorrect. "
                "None or all answers are set as correct."
            )


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    formset = AnswerAdminFormSet


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "question_type",
        "question_type_name",
        "question_type_description",
        "description",
    )
    list_select_related = (
        "question_type",
    )
    inlines = (
        AnswerInline,
    )
    empty_value = "-- empty --"


class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "description",
    )
    empty_value = "-- empty --"


class QuizAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "session_key",
        "is_completed",
        "score",
    )
    list_select_related = (
        "user",
    )
    readonly_fields = (
        "user",
        "session_key",
        "is_completed",
        "score",
        "questions",
    )
    empty_value = "-- empty --"


class AnswerGivenAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "quiz",
        "question",
        "answer",
        "is_correct",
    )
    list_select_related = (
        "quiz",
        "question",
        "answer",
    )
    empty_value = "-- empty --"


class QuestionCollectionAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "description",
    )
    filter_horizontal = (
        "collection_questions",
    )
    empty_value = "-- empty --"


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionType, QuestionTypeAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(AnswerGiven, AnswerGivenAdmin)
admin.site.register(QuestionCollection, QuestionCollectionAdmin)
