from django.views import generic


class UserStatsView(generic.TemplateView):
    template_name = 'user_stats.html'
