# hybah/settings.py

import os
from pathlib import Path
import dj_database_url # type: ignore

# --- Configuration de base ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Configuration pour la Production (Render.com) ---
# La clé secrète est lue depuis les variables d'environnement du serveur.
# Si elle n'est pas trouvée, une clé par défaut est utilisée (pour le développement local).
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-votre-ancienne-cle-par-defaut')

# DEBUG est True seulement si la variable d'environnement DEBUG est 'true'.
# Sur Render, elle ne sera pas définie, donc DEBUG sera False.
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Hôtes autorisés
ALLOWED_HOSTS = []
# On ajoute automatiquement l'URL de notre site sur Render.com
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# --- Applications installées ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'comptes',
    'salles',
    'reservations',
    'gateaux',
]

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Whitenoise pour servir les fichiers statiques en production
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware', # Une seule fois
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hybah.urls'

# --- Templates ---
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

WSGI_APPLICATION = 'hybah.wsgi.application'

# --- Base de données ---
# Cette configuration intelligente utilise la base de données de Render si disponible,
# sinon, elle utilise votre fichier db.sqlite3 local.
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# --- Internationalisation ---
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Fichiers Statiques (CSS, JS) ---
STATIC_URL = 'static/'
# Dossier où Django va chercher vos fichiers statiques (votre dossier 'static/')
STATICFILES_DIRS = [BASE_DIR / 'static']
# Dossier où 'collectstatic' va copier tous les fichiers pour la production
STATIC_ROOT = BASE_DIR / 'staticfiles_production'

# --- Fichiers Média (Images uploadées) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- Configuration pour Whitenoise (production) ---
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# --- Divers ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'