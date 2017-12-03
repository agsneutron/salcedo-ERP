
ALLOWED_HOSTS = ['*']
DEBUG = True
LOCAL_SETTINGS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'salcedo_erp_db',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '',
    }
}
