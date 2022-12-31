from django import forms
from .models import Diary
from django_ckeditor_5.widgets import CKEditor5Widget
from datetime import date
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from loguru import logger

class DiaryForm(ModelForm):

    @logger.catch
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].required=False
        self.fields['title'].required=False

    class Meta:
        model = Diary
        fields = ['date', 'title', 'text']

        widgets = {
            "date": forms.DateInput(format=('%Y-%m-%d'),
                                    attrs={'type': 'date',
                                            'class':'form-control w-25'}),
                                            
            "title": forms.TextInput(attrs={'class': 'form-control'}),
            "text": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }

    #cke editor doesn't work without this
    def clean_text(self):
        text = self.cleaned_data['text']
        if text == "":
            raise ValidationError('Дневник пуст')
        return text
