# Imports Django's default authentication backend.
# We're inheriting from it so we get check_password and
# user_can_authenticate methods for free — we only
# override authenticate().
# Imports a Django helper function. Instead of importing our
# User model directly, get_user_model() looks up whatever model
# is set in AUTH_USER_MODEL in settings.py. This is the recommended
# approach because if someone swaps the user model later, this still
# works — a direct import would break.
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# Calls the function at module load time and stores the result.
# This is intentional — you call it once at the top rather than
# inside authenticate() on every login attempt, so Django doesn't
# repeat that settings lookup on every request.
User = get_user_model()


# Don't forget to wire it up in settings.py to AUTHENTICATION_BACKENDS
class AuthWithEmailOrUsernameBackend(ModelBackend):
    # The method Django calls when authenticate() is invoked anywhere in your code.
    # The signature is a Django contract — request is the current HTTP request,
    # username and password are the credentials passed in. **kwargs absorbs any extra
    # credentials other backends might pass (e.g. a token).
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Guard clause. If either credential is missing, bail out immediately and
        # return None — meaning "this backend can't authenticate this request."
        # Django then moves on to the next backend in AUTHENTICATION_BACKENDS.
        if username is None or password is None:
            return None

        # User.objects.get() can raise an exception if user has not been found
        # so we need to wrap in try-catch here.
        try:
            if "@" in username:
                # Match in case-insensitive way.
                # User.objects here is a User manager.
                user = User.objects.get(email__iexact=username)
            else:
                # Match in case-sensitive way.
                user = User.objects.get(username__exact=username)
        except User.DoesNotExist:
            return None

        # check_password(password) — method from AbstractBaseUser. It hashes the provided
        # password and compares it to the stored hash. Never compares raw passwords.
        # self.user_can_authenticate(user) — inherited from ModelBackend. Checks that the
        # user's is_active field is True. Blocks soft-deleted or banned accounts.
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None

    def user_can_authenticate(self, user):
        # Always allow to authenticate for now since we don't have is_active field
        # in our User model. If we ever want to have "inactive" functionality for users
        # we can add logic here.
        return True
