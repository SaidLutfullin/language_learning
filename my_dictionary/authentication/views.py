from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from common.mixins.access_mixins import LogoutRequiredMixin
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import RegisterUserForm, LoginUserForm, CustomUserChangeForm, CustomPasswordChangeForm
from .forms import User
from loguru import logger
from django.shortcuts import get_object_or_404
from dictionary.words_operation import get_dictionary_statistics
from diary.models import Diary
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

class RegisterUser(LogoutRequiredMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('login')


class LoginUser(LogoutRequiredMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'authentication/login.html'


class ChangePassword(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy("password_change_done")
    template_name = "authentication/change_password.html"
    form_class = CustomPasswordChangeForm


class ChangePasswordDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = "authentication/password_change_done.html"


@logger.catch
@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


class MyProfile(LoginRequiredMixin, TemplateView):
    template_name = 'authentication/my_profile.html'

    @logger.catch
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dictionary_statistics = get_dictionary_statistics(self.request.user.pk)
        context.update(dictionary_statistics)
        context['diary_entry_count'] = Diary.objects.filter(user_id=self.request.user.pk).count()
        return context


class MyProfileEdit(LoginRequiredMixin, UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'authentication/my_profile_edit.html'
    success_url = reverse_lazy('my_profile')

    @logger.catch
    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)
