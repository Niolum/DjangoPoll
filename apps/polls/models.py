from django.db import models
from django.forms import ValidationError
from mptt.models import MPTTModel, TreeForeignKey

from apps.users.models import User


class Poll(models.Model):
    name = models.CharField(verbose_name='Poll', max_length=64)
    count_questions = models.PositiveSmallIntegerField(
        verbose_name='Count questions', default=0
    )

    class Meta:
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'

    def __str__(self):
        return f"{self.id} {self.name}"


class UserPoll(models.Model):
    STATUS_CHOICES = (
        ('START', 'Start'),
        ('OVER', 'Over')
    )

    user = models.ForeignKey(User,  verbose_name='User', on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, verbose_name='Poll', on_delete=models.CASCADE)
    status = models.CharField(verbose_name='Status', choices=STATUS_CHOICES, default='START')

    class Meta:
        verbose_name = 'User poll'
        verbose_name_plural = 'User polls'
    
    def __str__(self):
        return f'{self.id} {self.poll} {self.user} {self.status}'


class Question(MPTTModel):
    text = models.TextField(verbose_name='Text of question')
    poll = models.ForeignKey(
        Poll,
        verbose_name='Poll',
        on_delete=models.CASCADE
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Parent question'
    )

    class MPTTMeta:
        order_insertion_by = ['text']

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return f"{self.id} {self.text}"

    def clean(self):
        if self.poll.question_set.count() >= self.poll.count_questions:
            error = 'Cannot create more questions than indicated in the field count_questions in Poll object'
            raise ValidationError(error)
        super(Question, self).clean()

    def save(self, *args, **kwargs):
        self.clean()
        super(Question, self).save(*args, **kwargs)


class Answer(models.Model):
    text = models.TextField(verbose_name='Text of answer')
    question = models.ForeignKey(
        Question,
        verbose_name='Question',
        on_delete=models.CASCADE
    )
    next_question = models.OneToOneField(
        Question,
        verbose_name='Next question',
        on_delete=models.CASCADE,
        related_name='previous_question',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    user = models.ForeignKey(User,  verbose_name='User', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, verbose_name='Answer', on_delete=models.CASCADE)
    user_poll = models.ForeignKey(
        UserPoll,
        verbose_name='User poll',
        on_delete=models.CASCADE,
        related_name='user_answers'
    )
    created_at = models.DateTimeField(verbose_name='Answer time', auto_now_add=True)

    class Meta:
        verbose_name = 'User answer'
        verbose_name_plural = 'User answers'
    
    def __str__(self):
        return f'{self.id} {self.answer} {self.user}'
