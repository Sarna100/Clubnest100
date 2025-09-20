from django.apps import AppConfig

class ClubnestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ClubNest'

    def ready(self):
        import ClubNest.signals
def ready(self):
    import ClubNest.signals
