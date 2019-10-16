"""
Django settings for olade project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't015o(5yo_)9+wq+t2g469@2i13!4ezwx*+-&^_lok9ae!za^j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Configuration to use custom user model
AUTH_USER_MODEL = 'users.User'

ALLOWED_HOSTS = ['68.183.198.69', 'localhost']


# Application definition

INSTALLED_APPS = [
    'olade.apps.SuitConfig',
    'rest_framework',
    'super_inlines',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'safedelete',
    'tinymce',
    'users',
    'courses',
    'discounts',
    'constance',
    'constance.backends.database',
    'configurations',
    'payments',
    'smart_selects',
    'widget_tweaks',
]

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_ADDITIONAL_FIELDS = {
    'password': ['django.forms.CharField', {
        'widget': 'django.forms.PasswordInput',
    }],
}

CONSTANCE_CONFIG = {
    'APP_EMAIL_ADDRESS': ('test@test.ng', 'Email address by the application to send out emails'),
    'APP_EMAIL_PASSWORD': ('test123', 'Password for application email address', 'password'),
    'HST_GST': (13, 'HST/GST value', int),
    'STRIPE_USERNAME': ('stripe', 'Username for Olade Stripe account'),
    'STRIPE_API_KEY': ('stripe', 'API key for Olade Stripe account', str),
    'ONE_DRIVE_API_KEY': ('one-drive', 'API key for Olade One Drive account', str),
    'MODULE_EXPIRY_DAYS': (7, 'Number of days before access to module is revoked', int)
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'olade.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'olade.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'olade',
        'USER': 'olade_user',
        'PASSWORD': 'olade_19',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
# Tell Django where to find static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

LOGIN_REDIRECT_URL = '/courses/my-courses'
LOGIN_URL = '/users/login'

# path to media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# mail settings
EMAIL_HOST = "smtp.outlook.office365.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# for smart selects
USE_DJANGO_JQUERY = True
