# Generated by Django 4.1.3 on 2022-12-11 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_remove_answergiven_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='is_passed',
            new_name='is_completed',
        ),
    ]