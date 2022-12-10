# Generated by Django 4.1.3 on 2022-12-07 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Question type', max_length=50, unique=True, verbose_name='name')),
                ('description', models.CharField(blank=True, help_text='Question type description', max_length=200, null=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Question type',
                'verbose_name_plural': 'Question types',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='Question description', max_length=1000, verbose_name='content')),
                ('question_type', models.ForeignKey(help_text='Question type', on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='questions.questiontype', verbose_name='question_type')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='Answer description', max_length=100, verbose_name='description')),
                ('is_correct', models.BooleanField(help_text='Is answer correct?', verbose_name='is_correct')),
                ('question', models.ForeignKey(help_text='Related question', on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='questions.question', verbose_name='question')),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
                'ordering': ('-id',),
            },
        ),
    ]
