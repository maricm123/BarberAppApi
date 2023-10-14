from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TimeSlot(models.Model):
    start = models.CharField(max_length=10)
    end = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.start