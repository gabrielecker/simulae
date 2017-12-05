from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django import forms


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        password = self.cleaned_data.get('password', '')
        confirm_password = self.cleaned_data.get('confirm_password', '')
        if not password == confirm_password:
            raise forms.ValidationError('Falha ao confirmar senha.')
        return super(RegisterForm, self).clean()


class LoginForm(forms.Form):
    username = forms.CharField(label='Nome de usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username', '')
        password = self.cleaned_data.get('password', '')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('Login ou senha incorreto(a).')
        return super(LoginForm, self).clean()
