from django.contrib import admin
from django.forms import ModelForm
from subjects.helpers import SVGAndImageFormField
from subjects.models import Subject, Topic, Reference


class TopicInline(admin.TabularInline):
    model = Topic


class SubjectForm(ModelForm):
    model = Subject
    field_classes = {
        'image_field': SVGAndImageFormField
    }


class SubjectAdmin(admin.ModelAdmin):
    form = SubjectForm
    inlines = [
        TopicInline
    ]


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Topic)
admin.site.register(Reference)
