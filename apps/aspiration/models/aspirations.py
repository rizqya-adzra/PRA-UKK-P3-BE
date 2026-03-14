from django.db import models
from apps.user.models import CoreUser
from utils.models import UUIDModel
from utils.report_id import generate_report_id
from apps.aspiration.models.categories import Category


class Aspiration(UUIDModel):
    STATUS_CHOICES = [
        ('menunggu', 'Menunggu'),
        ('selesai', 'Selesai'),
        ('proses', 'Proses'),
        ('dibatalkan', 'Dibatalkan'),
    ]
    report_id = models.CharField(
        max_length=20, 
        unique=True, 
        editable=False
    )
    user = models.ForeignKey(
        CoreUser, 
        on_delete=models.CASCADE, 
        related_name='asp_aspirations',
        db_column='user_id'
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='aspirations')
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    def save(self, *args, **kwargs):
        if not self.report_id:
            self.report_id = generate_report_id(Aspiration)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.report_id} ({self.title})"
    
    
class AspirationProgress(UUIDModel):
    admin = models.ForeignKey(
        CoreUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        limit_choices_to={'is_staff': True},
        related_name='processed_progress'
    )
    aspiration = models.ForeignKey(Aspiration, on_delete=models.CASCADE, related_name='progress_updates')
    status = models.CharField(max_length=50, choices=Aspiration.STATUS_CHOICES)
    description = models.TextField()

    class Meta:
        db_table = 'asp_aspiration_progress'
        verbose_name = "Aspiration Progress"
        verbose_name_plural = "Aspiration Progress"

    def __str__(self):
        admin_name = self.admin.email if self.admin else "System"
        return f"{self.aspiration.report_id} - {self.status} (By: {admin_name})"
    

class AspirationFile(UUIDModel):
    aspiration = models.ForeignKey(
        Aspiration, 
        related_name='attachments', 
        on_delete=models.CASCADE
    )
    progress = models.ForeignKey(
        AspirationProgress, 
        related_name='progress_attachments', 
        on_delete=models.CASCADE,
        null=True, 
        blank=True
    )
    file = models.FileField(upload_to='aspiration/attachments/')