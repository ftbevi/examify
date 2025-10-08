from .base import * # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        'ENGINE': "django.db.backends.postgresql",
        'NAME': os.environ.get("POSTGRES_DB", "teste"),
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get("POSTGRES_PORT", "5432"),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
