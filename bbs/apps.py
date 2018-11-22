from django.apps import AppConfig


class BbsConfig(AppConfig):
    name = 'bbs'

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import bbs.signals