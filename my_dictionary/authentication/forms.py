from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from .models import User

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'имя пользователя'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'имя'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                    'placeholder': 'пароль1'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                        'placeholder': 'пароль2'}))

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'first_name', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'пароль'}))


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('avatar','first_name', 'last_name', 'gender', 'username', 'email', 'language_learned','about_me')
        
        widgets = {
            "avatar": forms.ClearableFileInput(attrs={'class': 'form-control'}),
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            "gender": forms.Select(attrs={'class': 'form-select'}),
            "username": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.EmailInput(attrs={'class': 'form-control'}),
            "language_learned": forms.TextInput(attrs={'class': 'form-control'}),
            "about_me": forms.Textarea(attrs={'class': 'form-control'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta(PasswordChangeForm):
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

