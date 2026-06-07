from .base import *

DEBUG = True

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

# only show debug toolbar to requests from localhost
INTERNAL_IPS = ["127.0.0.1"]
