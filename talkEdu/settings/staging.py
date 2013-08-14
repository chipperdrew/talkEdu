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
)


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

from urlparse import urlparse
if os.environ.has_key('HEROKU_POSTGRESQL_IVORY_URL'):
    url = urlparse(os.environ['HEROKU_POSTGRESQL_IVORY_URL'])
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': url.path[1:],
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port,
    }


# Parse database configuration from $DATABASE_URL
#import dj_database_url
#DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}


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
