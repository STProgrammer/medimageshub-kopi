from django.apps import AppConfig


class DicomsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dicoms'

    def ready(self):
        import dicoms.signals
