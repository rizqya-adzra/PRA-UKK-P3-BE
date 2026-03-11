from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.user.models import CoreUser, CoreStudent, CoreAdmin

@receiver(post_save, sender=CoreUser)
def create_user_related_tables(sender, instance, created, **kwargs):
    if created:
        default_name = instance.email.split('@')[0]
        
        if instance.is_staff or instance.is_superuser:
            CoreAdmin.objects.create(
                user=instance,
                name=default_name
            )
        else:
            CoreStudent.objects.create(
                user=instance,
                name=default_name,
                rombel='Belum diatur',
                rayon='Belum diatur'
            )