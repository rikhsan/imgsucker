"""
Django settings for imgsucker project.

Generated by 'django-admin startproject' using Django 2.1.2.

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
SECRET_KEY = '^^$#e_)k(25l!psig^ggf+ol_2jc(90yg%wpn=!40)=&y0t53*'

# SECURITY WARNING: don't run with debug turned on in production!
import sys
DEBUG=False
if len(sys.argv)>1:
    if sys.argv[1] != 'runserver':
       DEBUG=True 

ALLOWED_HOSTS = ['localhost','178.128.110.195','is.rikhsan.com']


# Application definition

INSTALLED_APPS = [
    'sorl.thumbnail',
    'imgsucker',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'django_social_share',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'imgsucker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'imgsucker.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'imgsucker',
        'USER': 'root',
        'PASSWORD': 'Alakazam1234!',
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'


# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static")
# ]

STATIC_ROOT= os.path.join(BASE_DIR, 'static')
MEDIA_ROOT= os.path.join(BASE_DIR, 'media')
MEDIA_URL= "/media/"
AUTH_USER_MODEL = 'imgsucker.User'


LOGIN_URL = 'fr_login'
LOGOUT_URL = 'fr_logout'
LOGIN_REDIRECT_URL = 'fr_home'


# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY =  '891867053852-0464eurr0fbqh5cmpfghi23hmgdqrf0g.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET =  'NNSQlHen0DZtMX1Kynhkh6rl'
# LOGIN_REDIRECT_URL = '//'
# SOCIAL_AUTH__KEY = 
# SOCIAL_AUTH__SECRET = 

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY ='328002259187-4vltcgp2vjaffg3jlqb885mk2o9v5t9s.apps.googleusercontent.com'  #Paste CLient Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'zcJdYqv2NppDqMf_uhkNlb3N' #Paste Secret Key