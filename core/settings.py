"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from decouple import config
import cloudinary
from django.contrib.messages import constants as message_constants

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost','.vercel.app','.now.sh','573b-197-248-239-47.ngrok-free.app']
CSRF_TRUSTED_ORIGINS=["https://picha-safari-vercel.vercel.app","https://573b-197-248-239-47.ngrok-free.app" ]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd Party Apps
    'cloudinary',
    'crispy_forms',
    'crispy_bootstrap4',
    'rest_framework',
    'mpesa',
    'paypal.standard.ipn',
    # My Apps
    'users',
    'dashboard',
    'photo',
    'cart',
    'payment',
    'Pesapal',
]

AUTH_USER_MODEL = 'users.CustomUser'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
SECURE_CROSS_ORIGIN_OPENER_POLICY='same-origin-allow-popups'
ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = 'cart-home' 
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'core.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST'),
#         'PORT': config('DB_PORT'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'URL': config('DATABASE_URL'),
        'NAME': config('PGDATABASE'),
        'USER': config('PGUSER'),
        'PASSWORD': config('PGPASSWORD'),
        'HOST': config('PGHOST'),
        'PORT': config('PGPORT'),
    }
}

# if not DATABASES['default']['NAME']:
#     # Fallback to SQLite if no PostgreSQL settings provided
#     DATABASES['default'] = {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT=  os.path.join(BASE_DIR,'staticfiles_build', 'static')

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly"
    ]
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

cloudinary.config( 
  cloud_name = config('CLOUDINARY_CLOUD_NAME'), 
  api_key = config('CLOUDINARY_API_KEY'), 
  api_secret = config('CLOUDINARY_API_SECRET') 
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"

CRISPY_TEMPLATE_PACK = "bootstrap4"

SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

MESSAGE_TAGS = {
    message_constants.DEBUG: 'secondary',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger', 
}

MPESA_CONFIG = {
    'CONSUMER_KEY': config('MPESA_CONSUMER_KEY'),
    'CONSUMER_SECRET': config('MPESA_CONSUMER_SECRET'),
    'CERTIFICATE_FILE': None,
    'HOST_NAME': 'https://picha-safari-vercel.vercel.app',
    'PASS_KEY': config('MPESA_PASSKEY'),
    'SAFARICOM_API': 'https://sandbox.safaricom.co.ke',
    'AUTH_URL': '/oauth/v1/generate?grant_type=client_credentials',
    'SHORT_CODE': config('MPESA_SHORTCODE'),
    'TILL_NUMBER': None,
    'TRANSACTION_TYPE': 'CustomerBuyGoodsOnline',
}

# # The Mpesa environment to use
# # Possible values: sandbox, production

# MPESA_ENVIRONMENT = config('MPESA_ENVIRONMENT')

# # Credentials for the daraja app

# MPESA_CONSUMER_KEY = config('MPESA_CONSUMER_KEY')
# MPESA_CONSUMER_SECRET = config('MPESA_CONSUMER_SECRET')

# #Shortcode to use for transactions. For sandbox  use the Shortcode 1 provided on test credentials page

# MPESA_SHORTCODE = config('MPESA_SHORTCODE')

# # Shortcode to use for Lipa na MPESA Online (MPESA Express) transactions
# # This is only used on sandbox, do not set this variable in production
# # For sandbox use the Lipa na MPESA Online Shorcode provided on test credentials page

# MPESA_EXPRESS_SHORTCODE = config('MPESA_EXPRESS_SHORTCODE')

# # Type of shortcode
# # Possible values:
# # - paybill (For Paybill)
# # - till_number (For Buy Goods Till Number)

# MPESA_SHORTCODE_TYPE = config('MPESA_SHORTCODE_TYPE')

# # Lipa na MPESA Online passkey
# # Sandbox passkey is available on test credentials page
# # Production passkey is sent via email once you go live

# MPESA_PASSKEY = config('MPESA_PASSKEY')

# # Username for initiator (to be used in B2C, B2B, AccountBalance and TransactionStatusQuery Transactions)

# MPESA_INITIATOR_USERNAME = config('MPESA_INITIATOR_USERNAME')

# # Plaintext password for initiator (to be used in B2C, B2B, AccountBalance and TransactionStatusQuery Transactions)

# MPESA_INITIATOR_SECURITY_CREDENTIAL = config('MPESA_INITIATOR_SECURITY_CREDENTIAL')


# PAYPAL CREDS
PAYPAL_RECEIVER_EMAIL='sb-fvofw25957115@business.example.com'
PAYPAL_TEST = True
