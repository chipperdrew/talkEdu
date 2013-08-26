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



# Caching w/ staticfiles
from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage

class CachedS3BotoStorage(S3BotoStorage):
    """
    S3 storage backend that saves the files locally, too.
    """
    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        name = super(CachedS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name
