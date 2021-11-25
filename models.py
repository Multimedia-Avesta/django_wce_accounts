from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(('email address'), blank=False, unique=True)
    full_name = models.TextField(max_length=150, blank=True)

    def __str__(self):
        return '{} ({})'.format(self.full_name, self.email)

    # required for post_save receivers in ote so they only need to run if
    # the field of interest has been changed
    def save(self, *args, **kwargs):
        if self.pk:  # check we already have a version in the database
            old = User.objects.get(pk=self.pk)
            new = self
            changed_fields = []
            for field in User._meta.get_fields():
                field_name = field.name
                try:
                    if getattr(old, field_name) != getattr(new, field_name):
                        changed_fields.append(field_name)
                except Exception as ex:
                    pass
            kwargs['update_fields'] = changed_fields
        super().save(*args, **kwargs)
