from django.apps import AppConfig

from registration.signals import user_activated

from fuser.signals import check_domain

class FuserConfig(AppConfig):
    name = 'fuser'

    def ready(self):
        user_activated.connect(check_domain, dispatch_uid='registration.signals.user_activated')