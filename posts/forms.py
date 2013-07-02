from registration.forms import RegistrationForm
from django import forms
from django.forms import ModelForm
from .models import eduuser

# Add extra 'user_type' field to the new user registration form
class eduuserForm(forms.ModelForm):
    class Meta:
        model = eduuser
        fields = ('user_type',)

RegistrationForm.base_fields.update(eduuserForm.base_fields)
