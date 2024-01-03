from django import forms
from django.forms import ModelForm, Textarea, CheckboxSelectMultiple, ChoiceField
from .models import Article


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ArticleForm(ModelForm):
    image_field = MultipleFileField()
    class Meta:
        model = Article
        fields = ['title', 'anouncement', 'text', 'date','category', 'tags']
        widgets = {
            'anouncement': Textarea(attrs={'cols':90,'rows':2}),
            'text': Textarea(attrs={'cols': 90, 'rows': 3}),
            'tags': CheckboxSelectMultiple(),
        }
# Для выбора нескольких файлов.
