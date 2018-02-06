# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

#ADMINS = (("Teemu", "teemu.t.lehtinen@aalto.fi"),)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r#=r)@i3iucw1tak*3(!h8une%=r7-rif63)7f(5(gm+-@^-)0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
AUTH_LTI_LOGIN = {
    'ACCEPTED_ROLES': ['Instructor', 'TA'],
    'STAFF_ROLES': ['Instructor', 'TA']
}

AUTH_USER_MODEL = "accounts.RadarUser"


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrapform',
    'data',
    'accounts',
    'review',
    'aplus_client',
    'django_lti_login',
    'ltilogin',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TOKENIZER_CHOICES = (("skip", "Skip"), ("scala", "Scala"))
TOKENIZERS = {
    "skip": {
        "tokenize": "tokenizer.skip.tokenize",
        "separator": "###### %s ######"
    },
    "scala": {
        "tokenize": "tokenizer.scala.tokenize",
        "separator": "/****** %s ******/"
    },
    "python": {
        "tokenize": "tokenizer.python.tokenize",
        "separator": "###### %s ######"
    },
    "text": {
        "tokenize": "tokenizer.text.tokenize",
        "separator": "###### %s ######"
    },
    "java": {
        "tokenize": "tokenizer.java.tokenize",
        "separator": "/****** %s ******/"
    },
}

PROVIDER_CHOICES = (("a+", "A+"), ("filesystem", "File system"))
PROVIDERS = {
    "a+": {
        "hook": "provider.aplus.hook",
        "cron": "provider.aplus.cron",
        "reload": "provider.aplus.reload",
        "host": "http://localhost:8000",
        "token": "a90b16c4ebbd3f996ca69e2ef8df3a2b1973e7b0",
    },
    "filesystem": {
        "hook": "provider.filesystem.hook",
        "cron": "provider.filesystem.cron",
    },
}

REVIEW_CHOICES = ((-10, "False alert"), (0, "Unspecified match"), (5, "Suspicious match"), (10, "Plagiate"), (1, "Approved plagiate"))
REVIEWS = (
    { "value": REVIEW_CHOICES[4][0], "name": REVIEW_CHOICES[4][1], "class": "success" },
    { "value": REVIEW_CHOICES[0][0], "name": REVIEW_CHOICES[0][1], "class": "success" },
    { "value": REVIEW_CHOICES[1][0], "name": REVIEW_CHOICES[1][1], "class": "default" },
    { "value": REVIEW_CHOICES[2][0], "name": REVIEW_CHOICES[2][1], "class": "warning" },
    { "value": REVIEW_CHOICES[3][0], "name": REVIEW_CHOICES[3][1], "class": "danger" },
)

MATCH_ALGORITHM = "matcher.jplag.match"
MATCH_STORE_MIN_SIMILARITY = 0.2
MATCH_STORE_MAX_COUNT = 10

SUBMISSION_VIEW_HEIGHT = 30
SUBMISSION_VIEW_WIDTH = 5

AUTO_PAUSE_MEAN = 0.9
AUTO_PAUSE_COUNT = 50

CRON_STOP_SECONDS = 120

ROOT_URLCONF = 'radar.urls'

WSGI_APPLICATION = 'radar.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'django_lti_login.backends.LTIAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_REDIRECT_URL = 'index'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# Directory to store all the submitted files.
SUBMISSION_DIRECTORY = os.path.join(BASE_DIR, "submission_files")


LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'verbose': {
      'format': '[%(asctime)s: %(levelname)s/%(module)s] %(message)s'
    },
  },
  'handlers': {
    'console': {
      'level': 'DEBUG',
      'class': 'logging.StreamHandler',
      'stream': 'ext://sys.stdout',
      'formatter': 'verbose',
    },
    'email': {
      'level': 'ERROR',
      'class': 'django.utils.log.AdminEmailHandler',
    },
  },
  'loggers': {
    'radar': {
      'level': 'DEBUG',
      'handlers': ['email', 'console'],
      'propagate': True
    },
  },
}


try:
    from local_settings import *
    def merge_dict(a, b):
        for key in b:
            if isinstance(b[key], dict) and key in a and isinstance(a[key], dict):
                merge_dict(a[key], b[key])
            else:
                a[key] = b[key]
    for var in ["PROVIDERS_MERGE",]:
        if var in locals():
            merge_dict(PROVIDERS, locals()[var])
except ImportError:
    pass
