from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nome')
    icon = models.FileField(upload_to='subjects', verbose_name='Ícone', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Data de edição')
    active = models.BooleanField(default=True, verbose_name='Ativa')

    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    subject = models.ForeignKey(Subject, related_name='topics', verbose_name='Disciplina')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Data de edição')
    active = models.BooleanField(default=True, verbose_name='Ativa')

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'

    def __str__(self):
        return self.name


class Reference(models.Model):
    description = models.TextField(verbose_name='Descrição')
    image = models.ImageField(upload_to='references', verbose_name='Imagem')
    link = models.URLField(verbose_name='Link')
    topic = models.ForeignKey(Topic, related_name='references', verbose_name='Tópico')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Data de edição')
    active = models.BooleanField(default=True, verbose_name='Ativa')

    class Meta:
        verbose_name = 'Referência'
        verbose_name_plural = 'Referências'

    def __str__(self):
        return self.description
