from base import *

# Email SMTP
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'YouTalkEdu@gmail.com'
EMAIL_HOST_PASSWORD = get_env_var("TALKEDU_EMAIL_PASS")

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
