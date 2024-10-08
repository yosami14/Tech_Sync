"""
Django settings for techsync project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-oult_iuc2y*_ho2@m*3p6!q=_5%08(07l0(mfajb2&38awe3f3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    #channel
    'daphne',
    
    #ADMIN CHARTS
    'admin_tools_stats',
    'django_nvd3',
    
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Apps
    'ckeditor',
    #if u Encounter a error for signals or app 
    #'users.apps.UsersConfig',
    'techsync',
    'projects',
    'users',
    'group',
    'a_rtchat',
    'event',
    'features',
    'a_videoChat',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'techsync.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'techsync.context_processors.navbar_data',
            ],
        },
    },
]

# WSGI_APPLICATION = 'techsync.wsgi.application'
ASGI_APPLICATION = 'techsync.asgi.application'

# channel layer cofig
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/images/'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Defined the custom user(Abstract user) at userapp -> models
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = ['users.backends.EmailAuthBackend']


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'yosami2020@gmail.com'
EMAIL_HOST_PASSWORD = 'rxdu uite hxsv zzdl'


# CKEDITOR CONFIGS
CKEDITOR_UPLOAD_PATH = 'uploads/'
# CKEDITOR_CONFIGS = {
#     'default': {
#         'skin': 'moono',
#         'codeSnippet_theme': 'monokai',
#         'toolbar': 'all',
#         'extraPlugins': ','.join(
#             [
#                 'codesnippet','widget','dialog',
#             ]
#         ),
#     },
# }


JAZZMIN_SETTINGS = {
    "site_title": "TechSync Admin",
    "site_header": "TechSync",
    "site_brand": "TechSync",
    "site_logo": "images/logo.png",
    "login_logo": "images/logo s.png",
    
    # Welcome text on the login screen
    "welcome_sign": "Admin login",
        # Copyright on the footer
    "copyright": "TechSync",
    # Links to put along the top menu
    "topmenu_links": [
        {"app": "group"},
        {"app": "a_rtchat"},
        {"app": "event"},
        {"app": "projects"},
        {"app": "users"},
        {"name": "Analytics", "url": "/admin-charts"},  # new link
    ],
    
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": ["auth"],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "app_name.ChatGroup": "fas fa-comments",
        "app_name.GroupMessage": "fas fa-comment-dots",
    },

    #hide side menu and some apps
    # "hide_apps": ["auth", "group", "a_rtchat", "event", "projects", "users","admin_tools_stats"],
    "hide_apps": ["auth", "group", "a_rtchat"],
    "show_sidebar": False,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "simplex",
}


GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

# py manage.py graph_models --pydot -a -g -o my_project_visualized.png


# chatbot
# settings.py
from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, 'techsync/features/.env'))
load_dotenv(os.path.join(BASE_DIR, 'techsync/bot/.env'))
load_dotenv(os.path.join(BASE_DIR, 'techsync/event/.env'))


# Other settings...
# For development
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techsync.settings')