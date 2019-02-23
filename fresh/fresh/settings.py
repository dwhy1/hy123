"""
Django settings for fresh project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2q5j@#s=4mq2_4vc+=ez9-55%k-g_n8h91#@w4&@g_6&x30z7d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',  # 注册全文检索框架
    'tinymce',  # 富文本编辑器
    'cart',  # 购物车模块
    'goods',  # 商品模块
    'order',  # 订单模块
    'user',  # 用户模块
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

ROOT_URLCONF = 'fresh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'fresh.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fresh',
        'USER': 'root',
        'PASSWORD': '......',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

# django认证系统使用的模型类
AUTH_USER_MODEL = 'user.User'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# STATICFILES_DIRS = [
#   ("images",os.path.join(STATIC_URL, 'images').replace('\\', '/')),
#   ("css",  os.path.join(STATIC_URL, 'css').replace('\\', '/')),
#   ("js",  os.path.join(STATIC_URL, 'js').replace('\\', '/')),
# ]

# 富文本编辑器配置
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'width': 600,
    'height': 400,
}

# 配置session储存到redis
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# SESSION_REDIS_HOST = "127.0.0.1"
# SESSION_REDIS_PORT = 6379
# SESSION_REDIS_DB = 6
# SESSION_REDIS_PASSWORD = "123456"
# SESSION_REDIS_PREFIX = "session"

# 配置连接redis的对象
from redis import StrictRedis

REDIS_CONN = StrictRedis(host="127.0.0.1", password='123456', port="6379", db=1)

# 发送邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# SMTP服务地址
EMAIL_HOST = 'smtp.qq.com'
# 端口号
EMAIL_PORT = 25
# 发送邮件的邮箱
EMAIL_HOST_USER = '1349176744@qq.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'stccfejoauiejfha'
# 收件人看到的发件人
EMAIL_FROM = '天天生鲜<1349176744@qq.com>'

# 配置url地址
LOGIN_URL = "/user/login"

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         # 选中的数据库
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             # "PASSWORD":密码
#         }
#     }
# }

# 配置session的设置
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# SESSION_CACHE_ALIAS = "default"
# 全文检索框架的配置
HAYSTACK_CONNECTIONS = {
    'default': {
        # 使用whoosh引擎
        # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'ENGINE': 'goods.whoosh_cn_backend.WhooshEngine',
        # 索引文件路径
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}

# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
