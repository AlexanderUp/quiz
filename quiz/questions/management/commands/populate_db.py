import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from ._utils import (process_answers, process_collections,  # isort:skip
                     process_collections_m2m, process_question_types,  # isort:skip
                     process_questions)  # isort:skip

CSV_FILES = {
    "question_types.csv": process_question_types,
    "questions.csv": process_questions,
    "answers.csv": process_answers,
    "question_collections.csv": process_collections,
    "question_collection_questions.csv": process_collections_m2m,
}

CSV_FILES_DIR = settings.BASE_DIR / "data"


class Command(BaseCommand):
    help = "Populate DB with questions for testing."

    def handle(self, *args, **options):
        for file, func in CSV_FILES.items():
            self.stdout.write(f"Processing: {file} with {func}")

            path = CSV_FILES_DIR / file
            with open(path, encoding="utf-8") as source:
                csv_reader = csv.reader(source, delimiter=";")
                func(csv_reader)
            self.stdout.write(f"{file} processed!")
        self.stdout.write("DB populated!")
