from project.wsgi import application
from whitenoise import WhiteNoise
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
global_static_path = os.path.join(BASE_DIR, "static")
application = WhiteNoise(application, root=global_static_path, prefix='static/')
app = application
