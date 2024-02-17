from django.db import models
from django.forms import ValidationError
from mptt.models import MPTTModel, TreeForeignKey


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
