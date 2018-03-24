import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'SUPER_SECRET_KEY'

DB_PASSWORD = 'db_pass'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ADMINS = [('My Beloved Administrator', 'admin_mail')]

# SERVER_EMAIL = 'no-reply@example.org'

# Obligatoire, liste des host autorisés
ALLOWED_HOSTS = ['URL_SERVER']

if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'db_engine',
            'NAME': 'db_name',
            'USER': 'db_user',
            'PASSWORD': DB_PASSWORD,
            'HOST': 'db_host',
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Security settings, à activer une fois https en place
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_BROWSER_XSS_FILTER = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_AGE = 60 * 60 * 3

# EMAIL_HOST = 'MY_EMAIL_HOST'
# EMAIL_PORT = MY_EMAIL_PORT
