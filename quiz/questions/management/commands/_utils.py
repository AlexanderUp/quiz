from collections import defaultdict

from django.shortcuts import get_list_or_404, get_object_or_404

from questions.models import (Answer, Question, QuestionCollection,  # isort:skip
                              QuestionType)


def process_question_types(reader):
    header = None
    question_types = []
    for row in reader:
        if not header:
            header = row
            continue
        zipped_row = zip(header, row)
        zipped_row_dict = dict(zipped_row)
        question_types.append(QuestionType(**zipped_row_dict))
    QuestionType.objects.bulk_create(question_types)


def process_questions(reader):
    header = None
    questions = []
    for row in reader:
        if not header:
            header = row
            continue
        zipped_row = zip(header, row)
        zipped_row_dict = dict(zipped_row)
        question_type_id = zipped_row_dict.pop("question_type_id")
        question_type = get_object_or_404(QuestionType, pk=question_type_id)
        questions.append(
            Question(question_type=question_type, **zipped_row_dict)
        )
    Question.objects.bulk_create(questions)


def process_answers(reader):
    header = None
    answers = []
    for row in reader:
        if not header:
            header = row
            continue
        zipped_row = zip(header, row)
        zipped_row_dict = dict(zipped_row)
        question_id = zipped_row_dict.pop("question_id")
        question = get_object_or_404(Question, pk=question_id)
        answers.append(Answer(question=question, **zipped_row_dict))
    Answer.objects.bulk_create(answers)


def process_collections(reader):
    header = None
    collections = []
    for row in reader:
        if not header:
            header = row
            continue
        zipped_row = zip(header, row)
        zipped_row_dict = dict(zipped_row)
        collections.append(QuestionCollection(**zipped_row_dict))
    QuestionCollection.objects.bulk_create(collections)


def process_collections_m2m(reader):
    collections_m2m = defaultdict(list)
    first_row = True
    for row in reader:
        if first_row:
            first_row = False
            continue
        _, question_collection_id, question_id = row
        collection = collections_m2m[question_collection_id]
        collection.append(question_id)
    for question_collection_id, question_ids in collections_m2m.items():
        question_collection = get_object_or_404(
            QuestionCollection, pk=question_collection_id
        )
        questions = get_list_or_404(Question, pk__in=question_ids)
        question_collection.collection_questions.set(questions)
