"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

# WSGI (Web Server Gateway Interface) is a standard protocol that defines
# how a Python web application communicates with a web server.
# It's a contract/interface between Gunicorn and Django:
# Browser → Nginx → Gunicorn → WSGI → Django
#
# Nginx speaks HTTP — handles raw web traffic
# Gunicorn is a WSGI server — translates HTTP requests into Python function calls
# WSGI is the agreed interface between them
# Django is a WSGI application — receives Python objects, returns Python objects
#
# Without a standard like WSGI, every Python framework would need its own server
# and they wouldn't be interchangeable. Because Django implements WSGI, you can
# swap Gunicorn for any other WSGI server (like uWSGI) without changing Django at all.

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

application = get_wsgi_application()
