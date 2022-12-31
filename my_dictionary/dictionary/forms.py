from django import forms
from .models import Words
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from loguru import logger

class AddinWordForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['context'].required=False

    class Meta:
        model = Words
        fields = ['russian_word', 'foreign_word', 'context', 'asking_date']
        labels = {'russian_word': 'Слово по-русски:',
                'foreign_word': 'Перевод',
                'context': 'Контекст:',
                'asking_date': 'Когда начнем учить:'}
        widgets = {
            'russian_word': forms.TextInput(attrs={'class': 'form-control'}),
            'foreign_word': forms.TextInput(attrs={'class': 'form-control'}),
            'context': forms.TextInput(attrs={'class': 'form-control'}),
            'asking_date': forms.DateInput(format=('%Y-%m-%d'),
                                            attrs={'type': 'date',
                                                    'class':'form-control'}),
        }

    @logger.catch
    def clean_context(self):
            context = self.cleaned_data['context']
            foreign_word = self.cleaned_data['foreign_word']
            russian_word = self.cleaned_data['russian_word']
            if context != "":
                context_edited = context.replace(foreign_word, f'({russian_word})')
                #means that the context doesn't contain new word
                if context_edited == context:
                    raise ValidationError('Контекст не содержит изучаемого слова')
            return context


class AskingForm(forms.Form):
    answer = forms.CharField(label='Перевод:', widget=forms.TextInput(attrs={'class': 'form-control'}))


class EditingForm(AddinWordForm): 
    from_scratch = forms.BooleanField(label="Учить по-новой",
                                    required=False,
                                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input toggle'}))
