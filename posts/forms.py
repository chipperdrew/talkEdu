from django.forms import ModelForm
from .models import post


class postForm(ModelForm):
    class Meta:
        model = post
        fields = ('title', 'text',)

    def __init__(self, *args, **kwargs):
        super(postForm, self).__init__(*args, **kwargs)

        # Custom error if title is blank
        self.fields['title'].error_messages = {'required': 'Please enter a title'}
