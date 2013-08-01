from django.contrib.auth import get_user_model  #eduuser
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from registration.forms import RegistrationForm

MIN_PASSWORD_LENGTH = 8

class eduuserForm(ModelForm):
    """
    Get extra 'user_type' field to add to form for django-registration
    """
    class Meta:
        model = get_user_model()
        fields = ('user_type',)


class MinPassLengthRegistrationForm(RegistrationForm):
    """
    Overrides form in django-registration, but checks for minimum password
    length and shows custom error messages
    """
    def __init__(self, *args, **kwargs):
        super(MinPassLengthRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].error_messages = {'required': 'Please enter a username'}
        self.fields['email'].error_messages = {'required': 'Please enter a valid email address'}
        self.fields['password1'].error_messages = {'required': 'Please enter a password'}
        self.fields['password2'].error_messages = {'required': 'Please verify your password'}
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1', '')
        if len(password) < MIN_PASSWORD_LENGTH:
            raise ValidationError('Password must have at least %i characters' %
                                  MIN_PASSWORD_LENGTH)
        else:
            return password


MinPassLengthRegistrationForm.base_fields.update(eduuserForm.base_fields)


class MinPassChangeForm(PasswordChangeForm):
    """
    Overrides form in django-auth, but checks for minimum password length
    and shows custom error messages
    """
    def __init__(self, *args, **kwargs):
        super(MinPassChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].error_messages = {'required': 'Please enter your old password'}
        self.fields['new_password1'].error_messages = {'required': 'Please enter a new password'}
        self.fields['new_password2'].error_messages = {'required': 'Please verify your new password'}
    
    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1', '')
        if len(password) < MIN_PASSWORD_LENGTH:
            raise ValidationError('Password must have at least %i characters' %
                                  MIN_PASSWORD_LENGTH)
        else:
            return password

