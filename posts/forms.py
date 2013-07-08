from django.forms import ModelForm
from .models import post


class postForm(ModelForm):
    class Meta:
        model = post
        fields = ('title', 'text',)
