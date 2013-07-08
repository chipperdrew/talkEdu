from registration.forms import RegistrationForm
from django.contrib.auth import get_user_model  #eduuser
from django.forms import ModelForm

class eduuserForm(ModelForm):
    """
    Get extra 'user_type' field to add to form for django-registration
    """
    class Meta:
        model = get_user_model()
        fields = ('user_type',)

RegistrationForm.base_fields.update(eduuserForm.base_fields)
