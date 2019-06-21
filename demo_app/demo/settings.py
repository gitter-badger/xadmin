"""
Django settings for demo_app project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l!fafmjcqyn+j+zz1@2@wt$o8w8k(_dhgub%41l#k3zi2m-b%m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
LANGUAGES = (
    # ('en', _('English')),
    ('zh-hans', _('Chinese')),
)

ALLOWED_HOSTS = ['xadmin.guofeifei.com','127.0.0.1','localhost']

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_ROOT = os.path.abspath(os.path.join(SITE_ROOT, '../'))
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
STATIC_URL = '/static/'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'material',
    # 'material.frontend',
    # 'viewflow',
    # 'viewflow.frontend',
    'xadmin',
    'crispy_forms',
    'reversion',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'demo.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'demo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/
MEDIA_URL='/media/'
# MEDIA_ROOT='/home/user/media/'
MEDIA_ROOT = os.path.join(SITE_ROOT)
TEMPLATES[0]['OPTIONS']['context_processors'].append('django.template.context_processors.media')
LANGUAGE_CODE = 'en-AU'#'zh-hans'en-us

TIME_ZONE = 'Australia/Canberra'#'Asia/Shanghai' America/Chicago

USE_I18N = True
USE_L10N = True#FalseTrue
# DATETIME_FORMAT = 'd/m/Y H:i:s'
# #
# DATE_FORMAT = 'd/m/Y' #日/月/年

# USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

if DEBUG and 1==2:
    # django debug toolbar
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    DEBUG_TOOLBAR_CONFIG = {
        'JQUERY_URL': '//cdn.bootcss.com/jquery/2.1.4/jquery.min.js',
        # 或把jquery下载到本地然后取消下面这句的注释, 并把上面那句删除或注释掉
        #'JQUERY_URL': '/static/jquery/2.1.4/jquery.min.js',
        'SHOW_COLLAPSED': True,
        'SHOW_TOOLBAR_CALLBACK': lambda x: True,
    }


#邮件配置

EMAIL_HOST = 'smtp.163.com'                   #SMTP地址

EMAIL_PORT = 25                                 #SMTP端口

DEFAULT_FROM_EMAIL = 'guocdfeifei@163.com'       #用户收到邮件显示的邮箱

EMAIL_HOST_USER = 'guocdfeifei@163.com'       #我自己的邮箱

EMAIL_HOST_PASSWORD = '1212'                  #我的邮箱密码

EMAIL_SUBJECT_PREFIX = u'[lybbn]'            #为邮件Subject-line前缀,默认是'[django]'

EMAIL_USE_TLS = True                             #与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false

#管理员站点

SERVER_EMAIL = 'guocdfeifei@163.com'