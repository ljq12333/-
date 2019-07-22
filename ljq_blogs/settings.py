"""
Django settings for ljq_blogs project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))  #在这里直接将app文件指向apps文件夹
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
#发送邮件的邮箱
EMAIL_HOST_USER = '1905673854@qq.com'
#在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'wwhqysuzhgsrbfae'
#收件人看到的发件人
EMAIL_FROM = '1905673854@qq.com'
EMAIL_USE_SSL = True
# EMAIL_USE_TLS = True
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pw=1g^m++5v5uf4myg@7r%ye4+m91#2hrk!)gj8wf!c2%bn#2%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes',
                  'django.contrib.sessions', 'django.contrib.messages',
                  'django.contrib.humanize', 'django.contrib.staticfiles',
                  'comment', 'storm', 'user', 'common', 'djcelery', 'admin',
                  'haystack')

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)
#全文检索框架的配置 选择whoosh 搜索
HAYSTACK_CONNECTIONS = {
    'default': {
        #使用whoosh引擎
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
        #索引文件路径
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}
# 自動生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
ROOT_URLCONF = 'ljq_blogs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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
REST_FRAMEWORK = {
    'DEFAULT_VERSION':
    'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    'VERSION_PARAM':
    'version',
    'DEFAULT_PARSER_CLASSES':
    ['rest_framework.parsers.JSONParser', 'rest_framework.parsers.FormParser']
}
WSGI_APPLICATION = 'ljq_blogs.wsgi.application'
# AUTH_USER_MODEL = 'storm.Blog_User'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': 'lijianqiang1998',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',  # 缓存使用redis数据库储存
        'LOCATION':
        'redis://127.0.0.1:6379/2',  # 使用本地的6379端口(redis的默认端口)第五个数据库(redis共有16个数据库0-15)
        "OPTIONS": {
            "CLIENT_CLASS":
            "django_redis.client.DefaultClient",  # 使用django_redis的默认参数
        },
    },
}
# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
DEFAULT_FILE_STORAGE = 'fdfs.storage.FastDfs'
FDFS_SERVER_URL = 'http://www.ljjlh.xyz:8888/'