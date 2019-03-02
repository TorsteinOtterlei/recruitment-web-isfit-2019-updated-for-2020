from .base import *
#from decouple import config  # using python-decouple

DEBUG=True

ALLOWED_HOSTS += []

MIDDLEWARE += []

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = config('DJANGO_SECRET_KEY')  # This is good - Nicolaj
SECRET_KEY = '*o#&hk_xb@tga0cvru5ny&#djv5)8spo6)_s^=8vkphb345&gf'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

INSTALLED_APPS += []
