from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Language, Words


class LanguageAdminForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ("language_name",)

        widgets = {
            "language_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class AddinWordForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["context"].required = False

    start_learning = forms.BooleanField(
        label="Начать учить",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input toggle",
                                          "checked": "ture"}),
    )

    class Meta:
        model = Words
        fields = ["russian_word", "foreign_word", "context", "asking_date"]
        labels = {
            "russian_word": "Слово по-русски:",
            "foreign_word": "Перевод",
            "context": "Контекст:",
            "asking_date": "Когда начнем учить:",
        }
        widgets = {
            "russian_word": forms.TextInput(attrs={"class": "form-control"}),
            "foreign_word": forms.TextInput(attrs={"class": "form-control"}),
            "context": forms.TextInput(attrs={"class": "form-control"}),
            "asking_date": forms.DateInput(
                format=("%Y-%m-%d"), attrs={"type": "date", "class": "form-control"}
            ),
        }

    def clean_context(self):
        context = self.cleaned_data["context"]
        foreign_word = self.cleaned_data["foreign_word"]
        russian_word = self.cleaned_data["russian_word"]
        if context != "":
            context_edited = context.replace(foreign_word, f"({russian_word})")
            # means that the context doesn't contain new word
            if context_edited == context:
                raise ValidationError("Контекст не содержит изучаемого слова")
        return context


class EditingForm(AddinWordForm):
    start_learning = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input toggle"}),
    )


class Exporting(forms.Form):
    russian_word = forms.BooleanField(
        label="Русское слово",
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    foreign_word = forms.BooleanField(
        label="Перевод",
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    context = forms.BooleanField(
        label="Контекст",
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    box_number = forms.BooleanField(
        label="Номер коробки",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    asking_date = forms.BooleanField(
        label="Дата ближайшего повторения",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
