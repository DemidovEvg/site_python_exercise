from django import forms
from .models import *
from .views import *
from django.contrib.auth.forms import UserCreationForm
from .utils import *


class ExerciseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_published'].required = True
        self.fields['is_published'].initial = True
        self.fields['category'].empty_label = "Категория не выбрана"

    class Meta:
        model = Exercise
        fields = ['title', 'task_text', 'is_published', 'category', 'tag']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'task_text': forms.Textarea(
                attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tag': forms.SelectMultiple(
                attrs={'class': 'form-control'}),
        }

    def clean_task_text(self):
        task_text = self.cleaned_data['task_text']
        clean_task_text = clean_data_from_js(task_text)
        return clean_task_text


class CreateTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'slug']
