from django.contrib.auth.models import User
from django.db import models
from random import sample
from subjects.models import Subject, Topic


class Choice(models.Model):
    description = models.TextField(verbose_name='Descrição')
    image = models.ImageField(upload_to='choices', verbose_name='Imagem', null=True, blank=True)
    question = models.ForeignKey('Question', related_name='choices', verbose_name='Questão')
    correct = models.BooleanField(verbose_name='Correta')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Data de edição')
    active = models.BooleanField(default=True, verbose_name='Ativa')

    class Meta:
        verbose_name = 'Alternativa'
        verbose_name_plural = 'Alternativas'

    def __str__(self):
        return '{}...'.format(self.description[:30])


class Question(models.Model):
    description = models.TextField(verbose_name='Descrição')
    image = models.ImageField(upload_to='questions', verbose_name='Imagem', null=True, blank=True)
    value = models.FloatField(verbose_name='Valor')
    hint = models.TextField(verbose_name='Explicação')
    subjects = models.ManyToManyField(Subject, related_name='questions', verbose_name='Disciplinas')
    topics = models.ManyToManyField(Topic, related_name='questions', verbose_name='Tópicos')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Data de edição')
    active = models.BooleanField(default=True, verbose_name='Ativa')

    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'

    def __str__(self):
        return '{}...'.format(self.description[:30])

    @classmethod
    def get_random(cls, subjects, length):
        ids = [id for id in cls.objects.filter(subjects__in=subjects)
               .values_list('id', flat=True).distinct()]
        random_ids = sample(ids, length)
        return cls.objects.filter(id__in=random_ids)


class Exam(models.Model):
    questions = models.ManyToManyField(Question, related_name='exams', through='ExamQuestion',
                                       verbose_name='Questões')
    current = models.ForeignKey(Question, verbose_name='Questão atual', null=True, blank=True)
    user = models.ForeignKey(User, related_name='exams', verbose_name='Aluno')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Data de edição')
    active = models.BooleanField(default=True, verbose_name='Ativa')

    class Meta:
        verbose_name = 'Simulado'
        verbose_name_plural = 'Simulados'
        ordering = ['-id']

    @classmethod
    def create(cls, user, subjects=Subject.objects.filter(active=True), length=45):
        """
        Create exam based on subjects and length
        """
        questions = Question.get_random(subjects, length)
        exam = cls(user=user, current=questions.first())
        exam.save()
        for question in questions:
            ExamQuestion.objects.create(exam=exam, question=question)
        return exam

    @property
    def grade(self):
        points = [answer.choice.question.value for answer
                  in self.answers.filter(active=True, choice__correct=True)]
        return sum(points)

    def above_average(self, average=0.7):
        correct = self.answers.filter(active=True, choice__correct=True).count()
        return (correct / self.answers.count()) > average

    def change_question(self):
        """
        Move exam current question to another one
        """
        self.current = self.questions.filter(question__answered=False).first()
        self.save()


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, related_name='question')
    question = models.ForeignKey(Question, related_name='question')
    answered = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Data de edição')
    active = models.BooleanField(default=True, verbose_name='Ativa')

    class Meta:
        verbose_name = 'Questão do simulado'
        verbose_name_plural = 'Questões do simulado'

    def answer(self, choice):
        answer = Answer.objects.create(choice=choice, exam=self.exam)
        self.answered = True
        self.save()
        self.exam.change_question()
        return answer.is_correct


class Answer(models.Model):
    exam = models.ForeignKey(Exam, related_name='answers', verbose_name='Simulado')
    choice = models.ForeignKey(Choice, related_name='answers', verbose_name='Alternativa')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Data de edição')
    active = models.BooleanField(default=True, verbose_name='Ativa')

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'

    @property
    def is_correct(self):
        return self.choice.correct
