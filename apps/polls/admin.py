from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from apps.polls.models import Poll, Question, Answer


class AnswerNestedInline(NestedStackedInline):
    model = Answer
    extra = 0


class QuestionInline(NestedStackedInline):
    model = Question
    inlines = [AnswerNestedInline]
    extra = 0


class PollAdmin(NestedModelAdmin):
    list_display = ['id', 'name', 'count_questions']
    inlines = [
        QuestionInline
    ]

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"text": ["text"]}
    mptt_level_indent = 20
    list_display = ['id', 'text']
    inlines = [
        AnswerInline
    ]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)