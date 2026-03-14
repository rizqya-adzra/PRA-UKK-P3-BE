from django.db import models
from apps.user.models import CoreUser
from utils.models import UUIDModel
from apps.aspiration.models.aspirations import Aspiration
    
    
class Notification(UUIDModel):
    user = models.ForeignKey(CoreUser, on_delete=models.CASCADE, related_name='notifications', db_column='user_id')
    aspiration = models.ForeignKey(Aspiration, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'asp_notification'
        verbose_name = "Aspiration Notification"

    def __str__(self):
        return f"{self.user.email}: {'Read' if self.is_read else 'Unread'}"