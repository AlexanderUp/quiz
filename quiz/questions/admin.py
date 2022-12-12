from django.contrib import admin

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


class AnswerInline(admin.TabularInline):
    model = Answer


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
