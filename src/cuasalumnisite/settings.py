# Django settings for cuasalumnisite project.

DEV = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('James Sharp', 'james.sharp@cantab.net')
)

MANAGERS = ADMINS

if DEV:
    _dbname = "cuasalumni_dev"
    _dbpwd = "c137db67"
else:
    _dbname = "cuasalumni"
    _dbpwd = "]O43D|r"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': _dbname,                 # Or path to database file if using sqlite3.
        'USER': _dbname,                      # Not used with sqlite3.
        'PASSWORD': _dbpwd,                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-uk'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
STATIC_DOC_ROOT = '/Users/james/Development/cuasalumni/cuasalumnisite/media/'
if DEV:
    MEDIA_ROOT = STATIC_DOC_ROOT
else:
    MEDIA_ROOT = '/home/cuasalumni/webapps/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 's7gb0(qh=o=6=xdfj+&vjo(u#6$kr8&s&sh=16*_n#znhar5qs'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'cuasalumnisite.urls'

if DEV:
    TEMPLATE_DIRS = (
        # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        '/Users/james/Development/cuasalumni/cuasalumnisite/templates'
    )
else:
    TEMPLATE_DIRS = (
        # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        '/home/cuasalumni/django_templates/cuasalumni'
    )

INSTALLED_APPS = (
    'cuasalumnisite.hacks',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'tinymce', 
    'cuasalumnisite.news',
    'cuasalumnisite.events',
    'cuasalumnisite.members',
    'cuasalumnisite.home',
)

TEMPLATE_CONTEXT_PROCESSORS=(
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "cuasalumnisite.home.context_processors.settings"
)

NEWS_ARTICLES_PER_PAGE = 5

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'

AUTH_PROFILE_MODULE = 'members.member'

TINYMCE_COMPRESSOR = True
TINYMCE_DEFAULT_CONFIG = {
                          'relative_urls' : 'true',
                          'theme': 'advanced',
                          'theme_advanced_toolbar_location' : "top"
}

if DEV:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'cuasalumni'
EMAIL_HOST_PASSWORD = 'b0Wv,EL'
DEFAULT_FROM_EMAIL = 'cuasalumni@cuas-alumni.org.uk'
SERVER_EMAIL = 'cuasalumni@cuas-alumni.org.uk'
    
MY_CERT_ID = '92HFNXHSSQJ4L'

# Paypal details
if DEV:
    PAYPAL_USERNAME = 'james_1310306837_biz@gmail.com'
    PAYPAL_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
    PAYPAL_PDT_IDENTITY_TOKEN = '8vW2oPts7JI0rmxpCQdAPZ6dRcMCcuJbBr8-9eND3gbFCaQoSqRBiMNRzYO'
else:
    PAYPAL_USERNAME = 'paypal@cuas-alumni.org.uk'
    PAYPAL_URL = 'https://www.paypal.com/cgi-bin/webscr'
    PAYPAL_PDT_IDENTITY_TOKEN = 't4rbPeBa8Uqz7EK50hwixpdJTpNbs7T2HzIlkaPaLlAXwoO_y_ZT7g4Gc5a'
    
PAY_NOW_BUTTON_URL = 'https://www.paypalobjects.com/en_GB/i/btn/btn_paynowCC_LG.gif' 
SUBSCRIBE_BUTTON_URL= 'https://www.paypalobjects.com/en_US/GB/i/btn/btn_subscribeCC_LG.gif'
    
# Pricing details
ANNUAL_MEMBERSHIP_COST = 2
LIFE_MEMBERSHIP_COST = 30
