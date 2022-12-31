from django.shortcuts import render, redirect
from .models import Diary
from .forms import DiaryForm
from loguru import logger
from django.views.generic import ListView, FormView, DetailView, DeleteView
from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from datetime import date
from django.views.generic.edit import BaseUpdateView


class NewDay(LoginRequiredMixin, FormView):
    model = Diary
    form_class = DiaryForm
    template_name = 'diary/my_day.html'
    success_url = reverse_lazy('my_diary')
    initial = {'date':date.today()}
    pk_url_kwarg = "day"

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user_id = self.request.user.pk
        diary.save()
        return HttpResponseRedirect(self.get_success_url())


class EditDay(NewDay, BaseUpdateView):
    #not to change original date when unser is redacting day
    initial = {}
    
    @logger.catch
    def get_queryset(self):
        return Diary.objects.filter(user_id=self.request.user.pk)


class MyDiary(LoginRequiredMixin, ListView):
    model = Diary
    template_name = 'diary/my_diary.html'
    paginate_by = 20

    @logger.catch
    def get_queryset(self):
        return Diary.objects.filter(user_id=self.request.user.pk)


class ShowDay(LoginRequiredMixin, DetailView):
    model = Diary
    context_object_name = 'day'
    template_name = 'diary/show_day.html'
    pk_url_kwarg = "day"

    @logger.catch
    def get_queryset(self):
        return Diary.objects.filter(user_id=self.request.user.pk)


class DeleteDay(LoginRequiredMixin, DeleteView):
    model = Diary
    pk_url_kwarg = "day"
    success_url = reverse_lazy('my_diary')
    template_name = "diary/delete_day.html"

    @logger.catch
    def get_queryset(self):
        return Diary.objects.filter(user_id=self.request.user.pk)
