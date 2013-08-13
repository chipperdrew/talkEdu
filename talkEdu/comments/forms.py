from django import forms
from django.forms import ModelForm
from comments.models import comment


class commentForm(ModelForm):
    #Hidden value to get a child's parent
    parent = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'parent'}), required=False)

    class Meta:
        model = comment
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super(commentForm, self).__init__(*args, **kwargs)
        # Custom error if title is empty or just white spaces
        self.fields['content'].error_messages = {'required': 'Please enter a comment',
                                               'blank': 'Please enter a valid comment'}

    # Remove whitespace from content
    def clean_content(self):
        return self.cleaned_data['content'].strip()
