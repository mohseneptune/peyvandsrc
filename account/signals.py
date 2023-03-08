from account.models import Khosousiaat, Entezaaraat

def create_user_khosousiat_and_entezaaraat(sender, instance, created, *args, **kwargs):
    if created:
        Khosousiaat.objects.create(user=instance)
        Entezaaraat.objects.create(user=instance)