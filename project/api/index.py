import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'project')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

from django.core.asgi import get_asgi_application
application = get_asgi_application()
