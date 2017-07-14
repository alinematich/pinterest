from builtins import print
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.core.exceptions import ValidationError
from users.models import User

__author__ = 'ali-user'


class UserForm(forms.ModelForm):
    student_number = forms.RegexField(regex='[8-9][0-9]{7}')
    password = forms.SlugField(widget=forms.PasswordInput)
    first_name = forms.SlugField(required=True)
    last_name = forms.SlugField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        exclude = ('date_joined', 'username')

    def clean(self):
        super(UserForm, self).clean()
        u = self.cleaned_data.get('student_number')
        try:
            User.objects.get(username=u)
            self.add_error('student_number', ValidationError('user exists'))
        except User.DoesNotExist:
            self.cleaned_data['username'] = u