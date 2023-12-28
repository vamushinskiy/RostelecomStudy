from django import forms
from django.forms import ModelForm, Textarea, CheckboxSelectMultiple
from .models import Article

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'anouncement', 'text', 'date', 'tags']
        widgets = {
            'anouncement': Textarea(attrs={'cols':90,'rows':2}),
            'text': Textarea(attrs={'cols': 90, 'rows': 3}),
            'tags': CheckboxSelectMultiple(),
        }