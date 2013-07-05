from registration.forms import RegistrationForm
from django.forms import ModelForm
from .models import eduuser, post


class eduuserForm(ModelForm):
    """
    Get extra 'user_type' field to add to form for django-registration
    """
    class Meta:
        model = eduuser
        fields = ('user_type',)

RegistrationForm.base_fields.update(eduuserForm.base_fields)


class postForm(ModelForm):
    class Meta:
        model = post
        fields = ('title', 'text',)
