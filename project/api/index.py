import os
from django.core.asgi import get_asgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_asgi_application()
app = WhiteNoise(application, root=os.path.join(os.path.dirname(__file__), "..", "staticfiles"))
