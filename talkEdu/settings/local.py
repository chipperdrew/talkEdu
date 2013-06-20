from base import *

DEBUG = True

TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydb',
        #'USER': 'chipperdrew',
        'USER': get_env_var("TALKEDU_DB_USER"),
        #'PASSWORD': 'qu1.qu1.',
        'PASSWORD': get_env_var("TALKEDU_DB_PASS"),
        'HOST': '',
        'PORT': '',
    }
}
