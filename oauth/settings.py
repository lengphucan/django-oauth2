"""
Django settings for oauth project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%xx@49ucilo7eswi#t_poyc_1@b7sqroy+w__y-oo*+t(9fgl^"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",
    "oauth2_provider",
    "corsheaders",
    "rest_framework",
    "rest_framework_jwt",
    "knox",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    # "custom.permission.ScopeMiddleware",
    # "custom.middleware.OAuth2TokenMiddleware",
]

ROOT_URLCONF = "oauth.urls"

CORS_ORIGIN_ALLOW_ALL = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "oauth.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        # "oauth2_provider.contrib.rest_framework.TokenHasScope",
    ),
}

JWT_AUTH = {
    "JWT_RESPONSE_PAYLOAD_HANDLER": "my_django_project.utils.jwt_response_payload_handler",
}


AUTHENTICATION_BACKENDS = [
    "custom.oauth.CustomOAuth2Backend",
    "django.contrib.auth.backends.ModelBackend",
]
APPEND_SLASH = False

AUTH_USER_MODEL = "users.User"

LOGIN_URL = "/admin/login/"


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# OAUTH2 PROVIDER
OAUTH2_PROVIDER = {
    "PKCE_REQUIRED": False,
    # "OAUTH2_BACKEND_CLASS": "custom.oauth.CustomOAuthLibCore",
    # "OAUTH2_VALIDATOR_CLASS": "custom.oauth.CustomOAuth2Validator",
    "ACCESS_TOKEN_EXPIRE_SECONDS": 100000000000,  # 24 hours hoặc giá trị lớn hơn nếu cần
    "REFRESH_TOKEN_EXPIRE_SECONDS": None,  # Refresh token không hết hạn
    "SCOPES": {
        "access_denied": "Access Denied API",
        "access_allowed": "Access Allowed API",
    },
}