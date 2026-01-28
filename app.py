import os
from django.core.wsgi import get_wsgi_application

# Fallback for Render's default 'app:app' setting
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipereco.settings')

application = get_wsgi_application()
app = application
