from django.db.models.signals import pre_save
from django.conf import settings


def set_username(sender, instance, **kwargs):
    instance.username = instance.email


pre_save.connect(set_username, sender=settings.AUTH_USER_MODEL)
