from base import *

# MODIFIED VARS FROM BASE.PY
SITE_ROOT = dirname(dirname(abspath(__file__)))
SITE_NAME = basename(SITE_ROOT)

# STATIC FILES (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = 'static'
STATICFILES_DIRS = (
    join(SITE_ROOT, 'static'),
)


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
        'INDEX_NAME': 'documents',
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
