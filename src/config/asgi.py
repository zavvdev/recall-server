"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

# ASGI (Asynchronous Server Gateway Interface) is the official
# standard in Python that defines how web servers communicate with
# asynchronous web applications and frameworks. It is the modern
# successor to WSGI (Web Server Gateway Interface), which was historically
# used to handle synchronous requests one at a time.
#
# ASGI solves this:
# Worker 1: handling request → waiting for database → while waiting,
# handle another request → done One worker can handle multiple requests
# concurrently by doing other work while waiting for slow operations.
#
# ASGI also adds support for WebSockets, Long polling, HTTP/2.
# Stick with WSGI/Gunicorn unless you specifically need
# WebSockets / Realtime Features.
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

application = get_asgi_application()
