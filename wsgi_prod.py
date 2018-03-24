import os
import sys


# Activation de l'environnement virtuel
activate_env=os.path.join('INSTALL_PATH/env_site', 'bin/activate_this.py')
exec(compile(open(activate_env, "rb").read(), activate_env, 'exec'), {'__file__':activate_env})

# Ajout du répertoire du site au PATH
sys.path.append('INSTALL_PATH')
sys.path.append('INSTALL_PATH/site_tps')

# Les trucs par défaut de Django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "site_tps.settings")
application = get_wsgi_application()
