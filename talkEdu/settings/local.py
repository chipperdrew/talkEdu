from base import *

DEBUG = True

TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += (
    'debug_toolbar', # For debugging/speed checks
)

# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydb',
        'USER': get_env_var("TALKEDU_DB_USER"),
        'PASSWORD': get_env_var("TALKEDU_DB_PASS"),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

ALLOWED_HOSTS += [
    '.localhost',
    '.127.0.0.1'
]
