AWS_ACCESS_KEY_ID = CHANGE_THIS
AWS_SECRET_ACCESS_KEY = CHANGE_THIS
AWS_STORAGE_BUCKET_NAME = CHANGE_THIS

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': CHANGE_THIS,
        'USER': CHANGE_THIS,
        'PASSWORD': CHANGE_THIS,
        'HOST': 'localhost',
        'PORT': '',
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CHANGE_THIS

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["localhost","127.0.0.1", "0.0.0.0"]
