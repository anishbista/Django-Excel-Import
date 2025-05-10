"""
WSGI config for django_excel_import project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import django

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_excel_import.settings")
django.setup()

# Run migrations automatically
from django.core.management import call_command

call_command("migrate", interactive=False)

application = get_wsgi_application()
