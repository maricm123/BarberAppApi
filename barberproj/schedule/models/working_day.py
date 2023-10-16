from django.db import models
from django.contrib.auth import get_user_model
from .time_slot import TimeSlot

User = get_user_model()

class WorkingDay(models.Model):
    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    FIRST = 'first'
    SECOND = 'second'

    SHIFT_CHOICES = [
        (FIRST, 'First'),
        (SECOND, 'Second'),
    ]
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES, default=FIRST)

    reserved = models.BooleanField(default=False)


    def __str__(self) -> str:
        return f"{self.date} at {self.time_slot}"
    
    class Meta:
        unique_together = ('date', 'time_slot')