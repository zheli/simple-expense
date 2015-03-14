"""
WSGI config for expense_track project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "expense_track.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
