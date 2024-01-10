from django import forms
from .validators import acceptable_email
from django.core.validators import MinLengthValidator
from .models import Account
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, FileInput, NumberInput, Select

class ContactForm(forms.Form):
    name = forms.CharField(max_length=70,
                           validators=[MinLengthValidator(3)])
    email = forms.EmailField(validators=[acceptable_email])
    message = forms.CharField(widget=forms.Textarea)

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {'username': TextInput({'class': 'textinput form-control',
                                          'placeholder': 'username'}),
                   'email': EmailInput({'class': 'textinput form-control',
                                        'placeholder': 'email'}),
                   'first_name': TextInput({'class': 'textinput form-control',
                                            'placeholder': 'First name'}),
                   'last_name': TextInput({'class': 'textinput form-control',
                                           'placeholder': 'Last name'}),
                   }

# Форма редактирования аккаунта
class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['post', 'phone', 'address', 'telegram', 'account_image']
        widgets = {'phone': NumberInput({'class': 'textinput form-control',
                                       'placeholder': 'phone number'}),
                   'address': TextInput({'class': 'textinput form-control',
                                         'placeholder': 'address'}),
                   'telegram': TextInput({'class': 'textinput form-control',
                                          'placeholder': 'telegram'}),
                   'account_image': FileInput({'class': 'form-control',
                                               'placeholder': 'image'})
                   }

