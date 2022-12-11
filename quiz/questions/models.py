from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class QuestionType(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="name",
        help_text="Question type",
    )
    description = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="description",
        help_text="Question type description",
    )

    class Meta:
        verbose_name = "Question type"
        verbose_name_plural = "Question types"
        ordering = ("-pk",)

    def __str__(self):
        return f"{self.name[:settings.MAX_MODEL_OBJ_STR_LENGHT]}"


class Question(models.Model):
    question_type = models.ForeignKey(
        QuestionType,
        related_name="questions",
        on_delete=models.CASCADE,
        verbose_name="question_type",
        help_text="Question type",
    )
    description = models.CharField(
        max_length=1000,
        verbose_name="content",
        help_text="Question description",
    )

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ("-pk",)

    def __str__(self):
        return f"{self.description[:settings.MAX_MODEL_OBJ_STR_LENGHT]}"

    @admin.display(description="question_type_name")
    def question_type_name(self):
        return f"{self.question_type.name}"

    @admin.display(description="question_type_description")
    def question_type_description(self):
        return f"{self.question_type.description}"


class Answer(models.Model):
    """Possible answers for given question."""
    question = models.ForeignKey(
        Question,
        related_name="answers",
        on_delete=models.CASCADE,
        verbose_name="question",
        help_text="Related question",
    )
    description = models.CharField(
        max_length=100,
        verbose_name="description",
        help_text="Answer description",
    )
    is_correct = models.BooleanField(
        verbose_name="is_correct",
        help_text="Is answer correct?",
    )

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering = ("-pk",)

    def __str__(self):
        return f"{self.description[:settings.MAX_MODEL_OBJ_STR_LENGHT]}"

    @admin.display(description="question_type")
    def question_type(self):
        return f"{self.question.question_type}"

    @admin.display(description="question_description")
    def question_description(self):
        return f"{self.question.description}"


class Quiz(models.Model):
    user = models.ForeignKey(
        User,
        related_name="quizes",
        on_delete=models.CASCADE,
        verbose_name="user",
        help_text="User havig quiz",
    )
    session_key = models.CharField(
        max_length=40,
        verbose_name="session_key",
        help_text="Session key",
    )
    is_completed = models.BooleanField(
        verbose_name="is_completed",
        help_text="Is quiz completed?",
        default=False,
    )
    questions = models.ManyToManyField(
        to=Question,
        related_name="quizes",
        verbose_name="questions",
        help_text="Quiz questions",
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="score",
        help_text="Quiz total score",
        default=0,
    )

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizes"
        ordering = ("-pk",)

    def __str__(self):
        return f"Quiz({self.pk})"


class AnswerGiven(models.Model):
    """Answers given by tested user."""
    quiz = models.ForeignKey(
        Quiz,
        related_name="answers_given",
        on_delete=models.CASCADE,
        verbose_name="quiz",
        help_text="Related quiz",
    )
    question = models.ForeignKey(
        Question,
        related_name="answers_given",
        on_delete=models.CASCADE,
        help_text="Answer related question",
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        verbose_name="answer",
        help_text="Answer given by user",
    )

    class Meta:
        verbose_name = "AnswerGiven"
        verbose_name_plural = "AnswersGiven"
        ordering = ("-pk",)

    def __srt__(self):
        return f"AnswerGiven({self.pk})"
