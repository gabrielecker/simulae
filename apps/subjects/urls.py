from django.conf.urls import url
from subjects import views

urlpatterns = [
    url(r'^$', views.SubjectsView.as_view(), name='subject-list'),
    url(r'^detail/(?P<id>[0-9]+)/$', views.SubjectDetailView.as_view(), name='subject-detail'),
    url(r'^topic/(?P<id>[0-9]+)/$', views.TopicDetailView.as_view(), name='topic-detail'),
]
