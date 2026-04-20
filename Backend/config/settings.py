import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security key and debug mode setup using environment variables
# -------------------------------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Allowed hosts configuration
# -------------------------------------------------------------------------
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'backend'
]

# Application definition
# -------------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# -------------------------------------------------------------------------

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_CORE_DATABASE"),
        "USER": os.getenv("MYSQL_USER"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD"),
        "HOST": os.getenv("MYSQL_HOSTNAME"),
        "PORT": 3306,
    }
}

# Custom database URL for SQLAlchemy
DATABASE_CUSTOM_URL = os.getenv("DATABASE_CUSTOM_URL")

# Password validation
# -------------------------------------------------------------------------

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
# -------------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# -------------------------------------------------------------------------

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# Logging configuration
# -------------------------------------------------------------------------

# Construct base logs directory and subdirectories for Django and DatabaseManager
LOGS_BASE_DIR = os.path.join(BASE_DIR, 'logs')
current_date = datetime.now().strftime('%Y-%m-%d')

# Construct specific paths for Django and DatabaseManager logs
DB_LOG_DIR = os.path.join(LOGS_BASE_DIR, 'db_manager', current_date)
DJANGO_LOG_DIR = os.path.join(LOGS_BASE_DIR, 'django', current_date)

# Ensure the log directories exist
os.makedirs(DB_LOG_DIR, exist_ok=True)
os.makedirs(DJANGO_LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] [{asctime}] [{name}.{module}] - {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{asctime}] [{levelname}] - {message}',
            'style': '{',
            'datefmt': '%H:%M:%S',
        },
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] - {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'django_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(DJANGO_LOG_DIR, 'django.log'),
            'when': 'midnight',     
            'interval': 1,          
            'backupCount': 30,      
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'db_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(DB_LOG_DIR, 'db_manager.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        # Default Django logger
        'django': {
            'handlers': ['console', 'django_file'],
            'level': 'INFO',
            'propagate': True,
        },
        # Custom logger for Django server logs
        'django.server': {
            'handlers': ['django.server', 'django_file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Custom logger for DatabaseManager
        'db_manager': {
            'handlers': ['console', 'db_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}