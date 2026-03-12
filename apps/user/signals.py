from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.user.models import CoreUser, CoreAdmin

@receiver(post_save, sender=CoreUser)
def create_user_related_tables(sender, instance, created, **kwargs):
    if created:        
        if instance.is_staff or instance.is_superuser:
            default_name = instance.email.split('@')[0]
            CoreAdmin.objects.create(
                user=instance,
                defaults={'name': default_name}
            )