from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # --- NEW: Tell Django to wake up the signals! ---
    def ready(self):
        import accounts.signals