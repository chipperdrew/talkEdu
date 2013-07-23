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
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1', '')
        if len(password) < self.min_password_length:
            raise ValidationError('Password must have at least %i characters' %
                                  self.min_password_length)
        else:
            return password


MinPassLengthRegistrationForm.base_fields.update(eduuserForm.base_fields)
