# Django settings for formd project.
import os

cwd = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), x)

ADMINS = (
    ('Stuart Kelly', 'stuart.leigh83@gmail.com.com'),
)

MANAGERS = ADMINS

AUTH_USER_MODEL = 'account.User'

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': '',
    },
}

EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
FROM_EMAIL = "postmaster@formd.io"
WELCOME_EMAIL_TEMPLATE = "formd-welcome"

ALLOWED_HOSTS = ['*']

TIME_ZONE = 'Europe/London'

LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

USE_I18N = False

USE_L10N = False

USE_TZ = True

MEDIA_ROOT = ''

STATIC_ROOT = cwd('../public')

STATICFILES_DIRS = (
    cwd('../static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '!e&et)1iy)%9ji@jus=@@jq0$vo14fy@1_1&rnde(!^a+!qz5#'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

CORS_URLS_REGEX = '^/api/v0/message/$'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'concept.middleware.CorsMiddleware',
)

ROOT_URLCONF = 'formd.urls'

WSGI_APPLICATION = 'formd.wsgi.application'

TEMPLATE_DIRS = (
    cwd('../templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'account',
    'plan',
    'concept',
    'south',
    'django_rq',
    'djrill',
)

LOGIN_URL = '/log-in/'

from environment import *
