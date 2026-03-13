from django.apps import AppConfig


class AspirationConfig(AppConfig):
    name = 'apps.aspiration'
    
    def ready(self):
        import apps.aspiration.signals
