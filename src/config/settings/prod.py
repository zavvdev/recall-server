from .base import *

DEBUG = False

# If True, the SecurityMiddleware redirects all non-HTTPS requests to HTTPS
# (except for those URLs matching a regular expression listed in SECURE_REDIRECT_EXEMPT).
SECURE_SSL_REDIRECT = True

# Whether to use a secure cookie for the session cookie. If this is set to True,
# the cookie will be marked as “secure”, which means browsers may ensure that
# the cookie is only sent under an HTTPS connection.
SESSION_COOKIE_SECURE = True

# Whether to use a secure cookie for the CSRF cookie. If this is set to True,
# the cookie will be marked as “secure”, which means browsers may ensure that
# the cookie is only sent with an HTTPS connection.
CSRF_COOKIE_SECURE = True

# Some browsers will try to guess the content types of the assets that they fetch,
# overriding the Content-Type header. While this can help display sites with improperly
# configured servers, it can also pose a security risk. If your site serves user-uploaded
# files, a malicious user could upload a specially-crafted file that would be interpreted
# as HTML or JavaScript by the browser when you expected it to be something harmless.
# To prevent the browser from guessing the content type and force it to always use the type
# provided in the Content-Type header, you can pass the X-Content-Type-Options: nosniff header.
# SecurityMiddleware will do this for all responses if the SECURE_CONTENT_TYPE_NOSNIFF setting
# is True.
SECURE_CONTENT_TYPE_NOSNIFF = True

# Tells browsers to always use HTTPS for your site and never HTTP. Once a browser sees this header
# it will refuse to connect over HTTP for the duration you specify.
# 31536000 = 1 year in seconds.
# One important warning — HSTS is hard to undo. Once a browser caches it, it will refuse
# HTTP connections for the full year.
# Never enable it before you have HTTPS properly working
# Start with a small value like 3600 (1 hour) to test first
# Only bump it to 31536000 when you're confident everything works.
SECURE_HSTS_SECONDS = 31536000
# Extends that same HTTPS-only rule to all your subdomains. Without it, someone could attack you
# through an insecure subdomain even if your main domain is locked down.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
