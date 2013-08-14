from registration.forms import RegistrationFormUniqueEmail
from accounts.forms import eduuserForm, check_pass_length

class MinPassLengthRegistrationForm(RegistrationFormUniqueEmail):
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
        self.fields['user_type'].label = "What best describes you?"


    def clean_password1(self):
        return check_pass_length(self, 'password1')


MinPassLengthRegistrationForm.base_fields.update(eduuserForm.base_fields) 
