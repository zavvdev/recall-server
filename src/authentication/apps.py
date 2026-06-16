# This file is Django's way of letting an app configure itself when Django starts up.

from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    # name = 'authentication' tells Django the Python import path of this app,
    # so Django knows where to find its models, migrations, templates, etc.
    # This is what INSTALLED_APPS actually points to.
    name = "authentication"
