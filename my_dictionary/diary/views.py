from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, FormView, ListView
from django.views.generic.edit import BaseUpdateView
from loguru import logger

from diary.forms import DiaryForm
from diary.models import Diary


class NewDay(LoginRequiredMixin, FormView):
    model = Diary
    form_class = DiaryForm
    template_name = "diary/my_day.html"
    # success_url = reverse_lazy("my_diary")
    initial = {"date": date.today()}
    pk_url_kwarg = "day"

    def get_success_url(self):
        return reverse_lazy("edit_day", kwargs={"day": self.kwargs.get("day")})

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user_id = self.request.user.pk
        diary.language = self.request.user.language_learned
        diary.save()
        return HttpResponseRedirect(self.get_success_url())


class EditDay(NewDay, BaseUpdateView):
    # not to change original date when unser is redacting day
    initial = {}

    @logger.catch
    def get_queryset(self):
        return Diary.objects.filter(
            user_id=self.request.user.pk, language=self.request.user.language_learned
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editing"] = True
        return context


class MyDiary(LoginRequiredMixin, ListView):
    model = Diary
    template_name = "diary/my_diary.html"
    paginate_by = 10

    @logger.catch
    def get_queryset(self):
        return Diary.objects.filter(
            user_id=self.request.user.pk, language=self.request.user.language_learned
        )


class ShowDay(LoginRequiredMixin, DetailView):
    model = Diary
    context_object_name = "day"
    template_name = "diary/show_day.html"
    pk_url_kwarg = "day"

    @logger.catch
    def get_queryset(self):
        return Diary.objects.filter(
            user_id=self.request.user.pk, language=self.request.user.language_learned
        )


class DeleteDay(LoginRequiredMixin, DeleteView):
    model = Diary
    pk_url_kwarg = "day"
    success_url = reverse_lazy("my_diary")
    template_name = "diary/delete_day.html"

    @logger.catch
    def get_queryset(self):
        return Diary.objects.filter(
            user_id=self.request.user.pk, language=self.request.user.language_learned
        )
