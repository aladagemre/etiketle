from contextlib import suppress

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "etiketle.users"
    verbose_name = _("Users")

    def ready(self):
        with suppress(ImportError):
            import etiketle.users.signals  # noqa F401
