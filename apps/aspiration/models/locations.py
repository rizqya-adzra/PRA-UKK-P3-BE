from django.db import models
from utils.models import UUIDModel


class Location(UUIDModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'asp_location'
        verbose_name = "Aspiration Location"

    def __str__(self):
        return f"{self.name}"