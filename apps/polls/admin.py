from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from apps.polls.models import Poll, Question, Answer, UserAnswer, UserPoll


class AnswerNestedInline(NestedStackedInline):
    model = Answer
    extra = 0
    fk_name = 'question'


class QuestionInline(NestedStackedInline):
    model = Question
    inlines = [AnswerNestedInline]
    extra = 0


class PollAdmin(NestedModelAdmin):
    list_display = ['id', 'name', 'count_questions']
    inlines = [QuestionInline]


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    fk_name = 'question'


class AnswerOnPreviousQuestionInline(admin.TabularInline):
    model = Answer
    fk_name = 'next_question'


class QuestionAdmin(DjangoMpttAdmin):
    mptt_level_indent = 20
    list_display = ['id', 'text']
    inlines = [AnswerInline, AnswerOnPreviousQuestionInline]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']


class UserPollAdmin(admin.ModelAdmin):
    pass


class UserAnswerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserPoll, UserPollAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
