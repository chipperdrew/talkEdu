from sys import path
import os
from os.path import abspath, basename, dirname, join, normpath
from django.core.exceptions import ImproperlyConfigured

SITE_ROOT = dirname(dirname(dirname(abspath(__file__))))
SITE_NAME = basename(SITE_ROOT)


def get_env_var(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_env_var("TALKEDU_SECRET_KEY")
AKISMET_KEY = get_env_var("TALKEDU_AKISMET_KEY")
ADMIN_URL = get_env_var("TALKEDU_ADMIN_URL")



AUTH_USER_MODEL = 'accounts.eduuser'
AUTHENTICATION_BACKENDS = ('accounts.backends.CaseInsensitiveModelBackend',)

# In order to receive email for HTTP 500 errors
ADMINS = (('Andrew', 'chipperdrew@gmail.com'),)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [] # AC: 7/13/13 Set this in production

# PREVENT NEW RELIC ERRORS
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'registration', # Easy user registration
    'south', # Database migration
    'haystack', # Search
    'honeypot', # Prevent spam
    'axes', # Limit login attempts
    'djangospam', # Prevent comment/post spam
    'djangosecure', # Security, like HtTPS and HSTS
    'picklefield',
    'posts',
    'accounts',
    'votes',
    'comments',
    'funct_tests',
    'registrationFix',
    'django.contrib.sitemaps',
    'storages', #Static file storing
)

SOUTH_TESTS_MIGRATE = False #South likes to throw errors on tests for some reason

# Honeypot name
HONEYPOT_FIELD_NAME = 'website'

# Required for django.contrib.sites
SITE_ID = 1

# Required for debug-toolbar 
INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

# Days to accept account activation
ACCOUNT_ACTIVATION_DAYS = 7

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware', # For compression
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.FailedLoginMiddleware',
    'accounts.middleware.ActiveUserMiddleware',
    'djangospam.cookie.middleware.SpamCookieMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
)

AXES_LOGIN_FAILURE_LIMIT = 5 # Num of login attempts until account is locked up

ROOT_URLCONF = 'talkEdu.urls'

WSGI_APPLICATION = 'talkEdu.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Denver'

USE_I18N = True

USE_L10N = True

USE_TZ = False


########### STATIC FILES (CSS, JavaScript, Images) #############
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    join(SITE_ROOT, 'static'),
)

STATICFILES_FINDERS = (
'django.contrib.staticfiles.finders.FileSystemFinder',
'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


######## TEMPLATES ###########
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


###### CACHING #######
def get_cache():
  try:
    os.environ['MEMCACHE_SERVERS'] = os.environ['MEMCACHIER_SERVERS'].replace(',', ';')
    os.environ['MEMCACHE_USERNAME'] = os.environ['MEMCACHIER_USERNAME']
    os.environ['MEMCACHE_PASSWORD'] = os.environ['MEMCACHIER_PASSWORD']
    return {
      'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'TIMEOUT': 500,
        'BINARY': True,
        'OPTIONS': { 'tcp_nodelay': True }
      }
    }
  except:
    return {
      'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
      }
    }

CACHES = get_cache()
