from django.shortcuts import render
from django.views.generic import ListView, UpdateView, FormView
from .models import Words
from .forms import AddinWordForm, AskingForm, EditingForm
from .words_operation import TestItem, get_words_list, get_dictionary_statistics
from loguru import logger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from datetime import date
from django.http import HttpResponseRedirect
import re

class AddingWord(LoginRequiredMixin, FormView):
    form_class = AddinWordForm
    template_name = 'dictionary/adding_word.html'
    success_url = reverse_lazy('adding_word')
    initial = {'asking_date':date.today()}

    @logger.catch
    def form_valid(self, form):
        word = form.save(commit=False)
        word.user_id = self.request.user.pk
        word.russian_word = re.sub(r'\<[^>]*\>', '', word.russian_word)
        word.foreign_word = re.sub(r'\<[^>]*\>', '', word.foreign_word)
        word.context = re.sub(r'\<[^>]*\>', '', word.context)

        word.save()
        return HttpResponseRedirect(self.get_success_url())


class EditWord(LoginRequiredMixin, UpdateView):
    form_class = EditingForm
    template_name = 'dictionary/edit.html'
    success_url = reverse_lazy('dictionary')
    initial = {'asking_date':date.today()}

    @logger.catch
    def get_object(self):
        return get_object_or_404(Words, pk=self.request.GET.get("id"), user_id=self.request.user.pk)

    @logger.catch
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        
        if 'delete' in self.request.POST:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        else:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    @logger.catch
    def form_valid(self, form):
        word = form.save(commit=False)
        #delete html tags from users strings just in case
        word.russian_word = re.sub(r'\<[^>]*\>', '', word.russian_word)
        word.foreign_word = re.sub(r'\<[^>]*\>', '', word.foreign_word)
        word.context = re.sub(r'\<[^>]*\>', '', word.context)

        if 'save' in self.request.POST:
            if form.cleaned_data['from_scratch']:
                word.save(update_fields = ["russian_word", "foreign_word", "context", "asking_date"])
            else:
                word.save(update_fields = ["russian_word", "foreign_word", "context"])
        return HttpResponseRedirect(self.get_success_url())


class Dictionary(LoginRequiredMixin, ListView):
    model = Words
    template_name = 'dictionary/dictionary.html'
    context_object_name = 'word_list'
    paginate_by = 3
    
    @logger.catch
    def get_queryset(self):
        search_query = self.request.GET.get("search-quesry", "")
        words_list = get_words_list(self.request.user.pk, search_query)
        return words_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        statistics = get_dictionary_statistics(self.request.user.pk)
        context.update(statistics)

        search_query = self.request.GET.get("search-quesry")
        if search_query is not None and search_query != "":
            context['search_query'] = self.request.GET.get("search-quesry")
        return context

@logger.catch
@login_required
def test(request):
    form = AskingForm(request.POST or None)
    #POST - mens user answered the question
    if request.method == 'POST' and form.is_valid():
        word = TestItem(request.user.pk)
        word.set_question(request.session.get('word'))
        word.send_users_answer(form.cleaned_data['answer'], request.session.get('help'), '<i><u>','</i></u>')
        if word.is_users_answer_correct():
            data = {
                'read_aloud':word.get_question()['read_aloud'],
                'russian_word':word.get_question()['russian_word'],
                'answer':word.get_question()['answer'],
            }
        else:
            #correct 'help' for user
            help = word.get_help()
            request.session['help'] = help
            
            data = {'help':help,
                    'question':word.get_question()['question'],
                    'form':form,
                    'read_aloud':'',  
            }
    else:
        #GET means new question or success
        form = AskingForm()
        word = TestItem(request.user.pk)
        #return False when words are over
        question_exists = word.make_question()
        if question_exists:
            request.session['word'] = word.get_question()
            request.session['help'] = ''
            data = {
                'help':'',
                'question':word.get_question()['question'],
                'form':form,
                'read_aloud':'',
            }
        else:
            return render(request, 'dictionary/success_text_page.html')
    return render(request, 'dictionary/test.html', data)


@logger.catch
@login_required
def cards(request):
    word = TestItem(request.user.pk)
    if request.method == 'POST':
        word_id = request.session.get('cart_word_id')
        if 'correct' in request.POST:
            word.send_card(word_id, True)
        else:
            word.send_card(word_id, False)
    question_exists = word.make_question()
    if question_exists:
        request.session['cart_word_id'] = word.get_question()['id']
        data = {
            'question':word.get_question()['question'],
            'answer':word.get_question()['answer'],
            'read_aloud':word.get_question()['read_aloud'],
            'russian_word':word.get_question()['russian_word']
        }
    else:
        return render(request, 'dictionary/success_text_page.html')
    return render(request, 'dictionary/cards.html', data)