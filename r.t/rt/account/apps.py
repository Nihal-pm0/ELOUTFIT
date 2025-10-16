from django.apps import AppConfig

class AccountConfig(AppConfig):  # Changed from AccountsConfig to AccountConfig
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'  # This should match your folder name
    verbose_name = 'Accounts'