from django.forms import ModelForm
from .models import comment


class commentForm(ModelForm):
    class Meta:
        model = comment
        fields = ('comment',)

    def __init__(self, *args, **kwargs):
        super(commentForm, self).__init__(*args, **kwargs)
        # Custom error if title is empty or just white spaces
        self.fields['comment'].error_messages = {'required': 'Please enter a comment',
                                               'blank': 'Please enter a valid comment'}

    # Remove whitespace from content
    def clean_comment(self):
        return self.cleaned_data['comment'].strip()
