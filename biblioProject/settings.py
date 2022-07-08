"""
Django settings for biblioProject project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i0vvy80_r)32d_ko(te=b$2x#m1dy*irzm50$(n2r$9wj0v_-b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalogo',
    'crispy_forms',
    #'django.contrib.gis',  ##para trabajar con Mapas (en este caso no hace falta poner esto porque igual funciona)
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'biblioProject.urls'

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

WSGI_APPLICATION = 'biblioProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


##trabajo con imagenes:
MEDIA_URL = '/media/' 
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')

"""
Donde:
MEDIA_URL --> es la ruta relativa a BASE_DIR, esta variable se utiliza para almacenar archivos multimedia (imagenes, videos, etc)

MEDIA_ROOT --> es la ruta absoluta, esta ruta se utiliza para recuperar archivos multimedia
    BASE_DIR --> apunta a la jerarquia superior del proyecto (la raiz), es decir, mi sitio. Si queremos usarlo tendremos que 
    usar el metodo "os" proporcionado por python.
"""

"""
Para traducir al español los nombres que le pusimos a nuestros campos del modelo (si es que lo pusimos en ingles) y 
mensajes de error (estan en ingles por defecto (por lo menos es asi con el campo password del modelo User que viene por defecto))

en el caso de que no nos guste la traduccion la modificamos en form realizando por ejemplo:
    password1 = forms.CharField(label='Contraseña', help_text="<ul><li>Su contraseña no puede ser demasiado similar a su otra información personal.</li> <li>Su contraseña debe contener al menos 8 caracteres.</li> <li>Su contraseña no puede ser una contraseña de uso común.</li> <li>Su contraseña no puede ser completamente numérica.</li></ul>")
    password2 = forms.CharField(label='Confirme contraseña', help_text="Ingrese la misma contraseña que antes, para verificación.", widget=forms.PasswordInput) # 

Nota: tambien te pone el admin en español (creo que te pone todo en español)
"""
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Lima'
USE_I18N = True