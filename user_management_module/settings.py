"""
Django settings for user_management_module project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import sys
import os
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0v#a82dva#+o=o0%kr6-bz=h5*#z-uo030se8gb77@si#08_g9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    
    'management.apps.ManagementConfig',
    # 'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'api',
    'rest_framework',
    'rest_framework_simplejwt',
    'sites',
    'ecommerce',
    'ckeditor',
    'ckeditor_uploader',
    'currencies',




    
]

# CRISPY_TEMPLATE_PACK = 'bootstrap4'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'user_management_module.urls'

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
                'sites.context_processors.get_sites',
                'ecommerce.context_processors.orders_cart_obj',
                'currencies.context_processors.currencies',


            ],
        },
    },
]

WSGI_APPLICATION = 'user_management_module.wsgi.application'

TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
# 'default': {
# 'ENGINE': 'django.db.backends.postgresql',
# 'NAME': 'management',
# 'USER': 'managementuser',
# 'PASSWORD': 'webnyxa@2020',
# 'HOST': 'localhost',
# 'PORT': '',
# }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE'  : 'django.db.backends.mysql', # <-- UPDATED line 
#         'NAME'    : 'webnyxa',                 # <-- UPDATED line 
#         'USER'    : 'root',                     # <-- UPDATED line
#         'PASSWORD': 'webnyxamysqldb',              # <-- UPDATED line
#         'HOST'    : 'localhost',                # <-- UPDATED line
#         'PORT'    : '3306',
#     }
# }



# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")


MEDIA_URL= '/media/'
MEIDIA_ROOT= os.path.join(BASE_DIR,'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_ACTIVE_FIELD='is_active'

EMAIL_FROM_USER = ""
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER ='comwebnyxa@gmail.com'
EMAIL_HOST_PASSWORD ='gxxmtkbiuxmeqhbx'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_MAIL_SUBJECT='conform your mail'
EMAIL_MAIL_HTML='email_body.html'
EMAIL_MAIL_PLAIN='mail_body.txt'
EMAIL_MAIL_TEMPLATE='conform_template.html'
EMAIL_PAGE_DOMAIN='http://127.0.0.1:8000/profile/'


# MAIL_DRIVER=Smtp
# MAIL_HOST=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USERNAME=dev@webnyxa.com
# MAIL_PASSWORD=Dev@2020!123
# MAIL_FROM=support@webnyxa.com
# MAIL_NAME=Webnyxa

# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'test@gmail.com'
# EMAIL_HOST_PASSWORD = 'test'
# EMAIL_PORT = 587


AUTH_USER_MODEL = 'management.User' 

LOGGING = {
    'version': 1,

    'disable_existing_loggers': False,

    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename':BASE_DIR /'management.log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'], 
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
CKEDITOR_UPLOAD_PATH = "uploads/"


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    
}

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source'],
            ['Form', 'Checkbox', 'Radio', 'TextField','Image', 'Textarea', 'Select', 'Button','HiddenField']

        ]
    }
}




DEFAULT_CURRENCY ='INR'

STRIPE_PUBLIC_KEY = ""
STRIPE_SECRET_KEY = ""
STRIPE_WEBHOOK_SECRET = ""
#domain EX: example.com
YOUR_DOMAIN = "webnyxa.com" 
##very important
#Set your Endpoint_URL in your stripe account WEBHOOK like this : https://YOUR_DOMAIN/orders/webhook/
#DEBUG_EMAIL_STRIPE
DEBUG_EMAIL = "comwebnyxa@gmail.com"
## End Stripe Settings ##

# ClientInfo For Aramex
ARAMEX_USERNAME = ""
ARAMEX_PASSWORD = ""
ARAMEX_VERSION = "v1.0"
ARAMEX_ACCOUNTNUMBER = ""
ARAMEX_ACCOUNTPIN = ""

ARAMEX_ACCOUNTENTITY = ""
ARAMEX_ACCOUNTCOUNTRYCODE = ""
ARAMEX_SOURCE = "24"

ARAMEX_PRODUCTGROUP = "EXP"
ARAMEX_PRODUCTTYPE = "PPX"


# #Smtp Email for recovery password
EMAIL_BACKEND = ''
SENDGRID_API_KEY = ''
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
EMAIL_SENDGRID = ""


# razorpay account ###
RAZORPAY_KEY_ID = ''
RAZORPAY_KEY_SECRET = ''

## paymob account ##
API_KEY = ""
#INTEGRATIONS_ID is integer data
PAYMENT_INTEGRATIONS_ID = None