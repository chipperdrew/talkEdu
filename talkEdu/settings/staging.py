from base import *

# AWS S3 bucket info
DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'
AWS_ACCESS_KEY_ID = os.environ['AWS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_KEY'] 
AWS_STORAGE_BUCKET_NAME = 'youtalkedu'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL

# Email SMTP
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'YouTalkEdu@gmail.com'
EMAIL_HOST_PASSWORD = get_env_var("TALKEDU_EMAIL_PASS")

INSTALLED_APPS += (
    'gunicorn', # Deployment
    'raven.contrib.django.raven_compat', # For Sentry add-on
)

# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': os.environ['SEARCHBOX_URL'],
        'INDEX_NAME': 'posts',
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS += ['*']

# SECURITY:
# Secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# For django-secure
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 63072000 #2 years
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_HTTPONLY = True


# Database
# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}
