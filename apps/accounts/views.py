from accounts.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic


class LoginView(generic.FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse('common:index'))
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            login(self.request, user)
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        args = self.request.GET.get('next', None)
        return args if args is not None else reverse_lazy('common:index')


class RegisterView(generic.FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('common:index')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse('common:index'))
        else:
            return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('common:index'))
