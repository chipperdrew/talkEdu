from django.forms import ModelForm
from .models import post


class postForm(ModelForm):
    class Meta:
        model = post
        fields = ('title', 'text',)

    def __init__(self, *args, **kwargs):
        super(postForm, self).__init__(*args, **kwargs)
        # Custom error if title is empty or just white spaces
        self.fields['title'].error_messages = {'required': 'Please enter a title',
                                               'blank': 'Please enter a valid title'}

    # Remove whitespace from title and text
    def clean_title(self):
        return self.cleaned_data['title'].strip()
    
    def clean_text(self):
        return self.cleaned_data['text'].strip()
