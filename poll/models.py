from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='متن سوال')
    pub_date = models.DateTimeField( verbose_name='تاریخ انتشار')

    def __str__(self):
        return str(self.id) + '- ' + self.question_text

    @admin.display(
        boolean = True,
        ordering = 'pub_date',
        description = 'published recently?',
    )
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - timedelta(days=2)


class Choise(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choise_text = models.CharField(max_length=200, verbose_name='متن گزینه')
    votes = models.IntegerField(default=0, verbose_name='تعداد رای')

    def __str__(self):
        return self.choise_text

class Person(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='نام')
    last_name = models.CharField(max_length=100, verbose_name='نام خانوادگی')
    national_code = models.CharField(max_length=10, verbose_name='کد ملی', unique = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Vote(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choise = models.ForeignKey(Choise, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['person', 'question'], name="poll_person_question_unique")
        ]
    