from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from exams import views

urlpatterns = [
    url(r'^answer/$', views.answer, name='answer'),
    url(r'^(?P<id>[0-9]+)?/?$', login_required(views.ExamDetailView.as_view()), name='exam-detail'),
    url(r'^start/$', views.start_exam, name='start-exam'),
    url(r'^list/$', login_required(views.UserExamsView.as_view()), name='exam-list'),
    url(r'^delete/(?P<id>[0-9]+)/$', login_required(views.ExamDeleteView.as_view()),
        name='delete-exam'),
    url(r'^new/$', login_required(views.ExamFormView.as_view()), name='create-exam'),
]
