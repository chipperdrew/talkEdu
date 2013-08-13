from django.contrib.auth import get_user_model  #eduuser
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

MIN_PASSWORD_LENGTH = 8

class eduuserForm(ModelForm):
    """
    Get extra 'user_type' field to add to form for django-registration
    """
    class Meta:
        model = get_user_model()
        fields = ('user_type',)

    def __init__(self, *args, **kwargs):
        super(eduuserForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].label = "What best describes you?"


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
        return check_pass_length(self, 'new_password1')


class MinPassResetForm(SetPasswordForm):
    """
    Overrides form in django-auth, but checks for minimum password length
    and shows custom error messages
    """
    def __init__(self, *args, **kwargs):
        super(MinPassResetForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].error_messages = {'required': 'Please enter a new password'}
        self.fields['new_password2'].error_messages = {'required': 'Please verify your new password'}
    
    def clean_new_password1(self):
        return check_pass_length(self, 'new_password1')


class CheckValidEmailPasswordResetForm(PasswordResetForm):
    """
    On password reset, makes sure a user exists with provided email, else error
    """
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            msg = "The provided email address is not registered to any user accounts. Please try a different email."
            raise ValidationError(msg)
        return email


## Helper function for checking minimum password length
def check_pass_length(self, provided_password):
    password = self.cleaned_data[provided_password]
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValidationError('Password must have at least %i characters' %
                              MIN_PASSWORD_LENGTH)
    return password

