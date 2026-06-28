from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"

    # Register signals.
    def ready(self):
        # Disable F401 in order to prevent ruff from
        # removing this unused import since we must
        # register signals here.
        import users.signals  # noqa: F401
