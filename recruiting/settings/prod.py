from .base import *

DEBUG=False

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

ALLOWED_HOSTS += ['.isfit.org']

MIDDLEWARE += []

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

INSTALLED_APPS += ['storages']

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
}


STATIC_URL = 'https://%s/%s%s' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION, STATIC_URL)
MEDIA_URL = 'https://%s/%s%s' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION, MEDIA_URL)

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_S3_OBJECT_PARAMETERS = {
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'CacheControl': 'max-age=94608000',
}
AWS_STORAGE_BUCKET_NAME = 'recruitment-web-isfit-2019'
AWS_S3_REGION_NAME = 'eu-west-1'  # e.g. us-east-2
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# Tell django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_LOCATION = 'static'


# HTTPS CONFIG
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
# Makes sure that csrf cookies are only set in https
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
