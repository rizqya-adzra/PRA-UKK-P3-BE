from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.user.models import CoreUser 
from .models import Aspiration, AspirationProgress, Notification

@receiver(post_save, sender=Aspiration)
def notify_aspiration_created(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            aspiration=instance,
            message=f"Aspirasi #{instance.report_id} Anda terkirim dan sedang diverifikasi",
        )

        admins = CoreUser.objects.filter(is_staff=True)
        
        admin_notifications = [
            Notification(
                user=admin,
                aspiration=instance,
                message=f"Aspirasi baru #{instance.report_id} menunggu verifikasi",
            ) for admin in admins
        ]
        
        Notification.objects.bulk_create(admin_notifications)

@receiver(post_save, sender=AspirationProgress)
def notify_progress_update(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.aspiration.user,
            aspiration=instance.aspiration,
            message=f"Status baru '{instance.status.upper()}' untuk Aspirasi #{instance.aspiration.report_id} Anda",
        )