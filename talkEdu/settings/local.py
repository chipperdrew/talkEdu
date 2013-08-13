from base import *

DEBUG = True

TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += (
    'debug_toolbar', # For debugging/speed checks
)


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydb',
        'USER': get_env_var("TALKEDU_DB_USER"),
        'PASSWORD': get_env_var("TALKEDU_DB_PASS"),
        'HOST': '',
        'PORT': '',
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

ALLOWED_HOSTS += [
    '.localhost',
    '.127.0.0.1'
]


def get_env_var(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)
    
SECRET_KEY = get_env_var("TALKEDU_SECRET_KEY")
AKISMET_KEY = get_env_var("TALKEDU_AKISMET_KEY")
ADMIN_URL = get_env_var("TALKEDU_ADMIN_URL")
