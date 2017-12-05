from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from stats import views

urlpatterns = [
    url(r'^user/$', login_required(views.UserStatsView.as_view()), name='user-stats')
]
