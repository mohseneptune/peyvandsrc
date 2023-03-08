from django.apps import AppConfig
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self) -> None:
        from account.signals import create_user_khosousiat_and_entezaaraat
        User = get_user_model()

        post_save.connect(create_user_khosousiat_and_entezaaraat, sender=User)
