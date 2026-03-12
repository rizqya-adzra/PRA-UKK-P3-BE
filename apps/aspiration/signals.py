from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Aspiration, AspirationProgress, Notification

@receiver(post_save, sender=Aspiration)
def notify_aspiration_created(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            aspiration=instance,
            message=f"Aspirasi Anda dengan Report ID {instance.report_id} berhasil terkirim. Mohon tunggu verifikasi admin."
        )

@receiver(post_save, sender=AspirationProgress)
def notify_progress_update(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.aspiration.user,
            aspiration=instance.aspiration,
            message=f"Update terbaru: Aspirasi {instance.aspiration.report_id} sekarang berstatus '{instance.status.upper()}'. Keterangan: {instance.description}"
        )