# Generated by Django 4.1.3 on 2022-12-12 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_alter_answergiven_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionset',
            name='set_questions',
            field=models.ManyToManyField(help_text='Questions in qeustion set', related_name='question_sets', to='questions.question', verbose_name='questions'),
        ),
    ]