import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

os.environ['DJANGO_SETTINGS_MODULE'] = 'futuShareDjango.settings'


sys.stdout = sys.stderr # Prevent crashes upon print

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


