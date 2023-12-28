from django import forms
from .validators import acceptable_email
from django.core.validators import MinLengthValidator

class ContactForm(forms.Form):
    name = forms.CharField(max_length=70,
                           validators=[MinLengthValidator(3)])
    email = forms.EmailField(validators=[acceptable_email])
    message = forms.CharField(widget=forms.Textarea)