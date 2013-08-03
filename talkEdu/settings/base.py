# TODO IN PRODUCTION ----- Change SECRET_KEY, Database user and pass

import os
from os.path import abspath, basename, dirname, join, normpath
from sys import path
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
SITE_ROOT = dirname(dirname(dirname(abspath(__file__))))
                                # SHOULD BE: django_codes/talkEdu
                                # In shell: from talkEdu import settings as S
SITE_NAME = basename(SITE_ROOT)


def get_env_var(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

AUTH_USER_MODEL = 'accounts.eduuser'
AUTHENTICATION_BACKENDS = ('accounts.backends.CaseInsensitiveModelBackend',)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

SECRET_KEY = get_env_var("TALKEDU_SECRET_KEY")

AKISMET_KEY = get_env_var("AKISMET_KEY")

DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [] # AC: 7/13/13 Set this in production


# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'registration', # Easy registration
    'disqus', # Commenting -- UNNECESSARY?!?
    'south', # Database migration
    'haystack', # Search
    'honeypot', # Prevent spam
    'axes', # Limit login attempts
    'debug_toolbar', # For debugging/speed checks
    'posts',
    'accounts',
    'votes',
    'comments',
    'funct_tests',
)

SOUTH_TESTS_MIGRATE = False #South likes to throw errors on tests for some reason


# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}

# Honeypot name
HONEYPOT_FIELD_NAME = 'website'

# Required for django.contrib.sites
SITE_ID = 1

# Required for debug-toolbar 
INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

ACCOUNT_ACTIVATION_DAYS = 7

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.FailedLoginMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'accounts.middleware.ActiveUserMiddleware',
)

AXES_LOGIN_FAILURE_LIMIT = 5 # Num of login attempts until account is locked up

ROOT_URLCONF = '%s.urls' % SITE_NAME

WSGI_APPLICATION = 'talkEdu.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Denver'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# STATIC FILES (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    normpath(join(SITE_ROOT, 'static')),
)

STATICFILES_FINDERS = (
'django.contrib.staticfiles.finders.FileSystemFinder',
'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# TEMPLATES
# See: https://docs.djangoproject.com
#               /en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    normpath(join(SITE_ROOT, 'templates')),
)
