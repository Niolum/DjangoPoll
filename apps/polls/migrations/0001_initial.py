# Generated by Django 5.0.1 on 2024-02-10 13:58

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Poll')),
                ('count_questions', models.PositiveSmallIntegerField(default=0, verbose_name='Count questions')),
            ],
            options={
                'verbose_name': 'Poll',
                'verbose_name_plural': 'Polls',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text of question')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='polls.question', verbose_name='Parent question')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.poll', verbose_name='Poll')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text of answer')),
                ('next_question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='previous_question', to='polls.question', verbose_name='Next question')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.question', verbose_name='Question')),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
        ),
    ]
