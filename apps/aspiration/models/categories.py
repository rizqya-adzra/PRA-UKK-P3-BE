from django.db import models
from utils.models import UUIDModel


class Category(UUIDModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'asp_category'
        verbose_name = "Aspiration Category"
        verbose_name_plural = "Aspiration Categories"

    def __str__(self):
        return f"{self.name}"