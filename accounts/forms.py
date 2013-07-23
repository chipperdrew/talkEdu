from django.contrib.auth import get_user_model  #eduuser
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from registration.forms import RegistrationForm


class eduuserForm(ModelForm):
    """
    Get extra 'user_type' field to add to form for django-registration
    """
    class Meta:
        model = get_user_model()
        fields = ('user_type',)


class MinPassLengthRegistrationForm(RegistrationForm):
    min_password_length = 8

    def __init__(self, *args, **kwargs):
        super(MinPassLengthRegistrationForm, self).__init__(*args, **kwargs)

        # Custom error if title is blank
        self.fields['username'].error_messages = {'required': 'Please enter a username'}
        self.fields['email'].error_messages = {'required': 'Please enter a valid email address'}
        self.fields['password1'].error_messages = {'required': 'Please enter a password'}
        self.fields['password2'].error_messages = {'required': 'Please verify your password'}
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1', '')
        if len(password) < self.min_password_length:
            raise ValidationError('Password must have at least %i characters' %
                                  self.min_password_length)
        else:
            return password


MinPassLengthRegistrationForm.base_fields.update(eduuserForm.base_fields)
