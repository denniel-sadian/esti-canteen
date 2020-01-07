"""
WSGI config for esticanteen project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

from dotenv import load_dotenv

import os

from django.core.wsgi import get_wsgi_application

load_dotenv(os.path.join(path, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'esticanteen.settings')

application = get_wsgi_application()
