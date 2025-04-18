from django import forms
from django.core.exceptions import ValidationError
from .models import *


class AddPostForm(forms.ModelForm):
    TITLE_MAX_LENGTH = 200 # макс. длина заголовка

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['cat'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Person
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']

        if len(title) > self.TITLE_MAX_LENGTH:
            raise ValidationError(f'Длина превышает {self.TITLE_MAX_LENGTH} символов')

        return title
