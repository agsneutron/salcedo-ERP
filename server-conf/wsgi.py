import os
import sys
import site

from django.core.wsgi import get_wsgi_application
 
os.environ['PYTHON_EGG_CACHE'] = '/eggCache'


# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/dev_tools/salcedo_env/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/var/www/html/erp')
sys.path.append('/var/www/html/erp/SalcedoERP')

sys.path.insert(0, '/home/erp')

# Activate your virtual env
activate_env = os.path.expanduser("/home/dev_tools/salcedo_env/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SalcedoERP.settings")

application = get_wsgi_application()