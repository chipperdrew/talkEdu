from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# If decide to change back to case sensitive -- delete this and
# AUTHENTICATION_BACKENDS settings in base.py
# Source: http://djangosnippets.org/snippets/1368/
class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = get_user_model().objects.get(username__iexact=username)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None
 
    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
