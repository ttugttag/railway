from pathlib import Path
import dj_database_url

# for environment
from environ import Env
env = Env()
Env.read_env()
ENVIRONMENT = env('ENVIRONMENT', default='production')

# Feature Toggle
DEVELOPER = env('DEVELOPER', default='')
STAGING = env('STAGING', default=False)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECRET_KEY = 'django-insecure-9lrlv6xa#v850ysn^t2x%5ac@ss_nhhu2(%6&x=!kqcs=p60#o'
SECRET_KEY = env('SECRET_KEY')
# ENCRYPT_KEY = b'5iywR4Xt-JgOzWTA3gMRHiykm3RbRn3mjDVKHA9dvA0='
ENCRYPT_KEY = env('ENCRYPT_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

# for environment
if ENVIRONMENT == 'development':
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = ["*"] 
# ALLOWED_HOSTS = ['localhost', '127.0.0.1', env("RENDER_EXTERNAL_HOSTNAME")]   
# ALLOWED_HOSTS = ['localhost', '127.0.0.1']
# CSRF_TRUSTED_ORIGINS =[ 'https://*.onrender.com']

INTERNAL_IPS = (
    '127.0.0.1',
    'localhost:8000'
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # for django-allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',   
    # for Cleanup
    'django_cleanup.apps.CleanupConfig',
    # for Clesitemaps
    'django.contrib.sitemaps',
    # django_htmx
    "django_htmx",
    # for honeypot theboss
    "admin_honeypot",
    
    # for media server
    'cloudinary_storage',
    'cloudinary',            
        
    'a_posts',
    'a_users',
    'a_features',
    'a_landingpages',   
]

# for django-allauth
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # for django-allauth
    "allauth.account.middleware.AccountMiddleware",
    # django_htmx
    "django_htmx.middleware.HtmxMiddleware",
    # whitenoise
    "whitenoise.middleware.WhiteNoiseMiddleware", 
    # a_landingpages
    'a_landingpages.middleware.landingpage_middleware',            
]

ROOT_URLCONF = 'a_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# for django-allauth
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'a_core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

POSTGRES_LOCALLY = False
if ENVIRONMENT == 'production' or POSTGRES_LOCALLY == True:
    # for extenal database 설정    
    DATABASES['default'] = dj_database_url.parse(env("DATABASE_URL"))

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

# USE_TZ = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS=[BASE_DIR / 'static']

# for whitenoise for collectstatic
STATIC_ROOT=BASE_DIR / 'staticfiles'

# for media
MEDIA_URL = 'media/'

# for media server
if ENVIRONMENT == "production" or POSTGRES_LOCALLY == True:
    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
            },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
            },
    }
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': env('CLOUD_NAME'),
        'API_KEY': env('API_KEY'),
        'API_SECRET': env('API_SECRET'),    
    }    
else:
    MEDIA_ROOT = BASE_DIR / 'media'
   
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = "/"

# for email authentication
if ENVIRONMENT == "production" or POSTGRES_LOCALLY == True:    
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = env('EMAIL_ADDRESS')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    # DEFAULT_FROM_EMAIL = 'Awesome'
    DEFAULT_FROM_EMAIL = f'Awesome {env("EMAIL_ADDRESS")}'
    ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True

# for blacklist
ACCOUNT_USERNAME_BLACKLIST = ['admin','accounts','profile','category','post','theboss']

