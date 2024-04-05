from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Author


@receiver(pre_save, sender=Author)
def populate_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.fullname)



