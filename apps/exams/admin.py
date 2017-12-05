from django.contrib import admin
from exams.models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline
    ]


admin.site.register(Choice)
admin.site.register(Question, QuestionAdmin)
