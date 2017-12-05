from django.views import generic
from subjects.models import Subject, Topic


class SubjectsView(generic.list.ListView):
    template_name = 'subject_list.html'
    model = Subject
    context_object_name = 'subjects'

    def get_queryset(self):
        return Subject.objects.filter(active=True)


class SubjectDetailView(generic.detail.DetailView):
    template_name = 'subject_detail.html'
    model = Subject
    context_object_name = 'subject'
    pk_url_kwarg = 'id'


class TopicDetailView(generic.detail.DetailView):
    template_name = 'topic_detail.html'
    model = Topic
    context_object_name = 'topic'
    pk_url_kwarg = 'id'
