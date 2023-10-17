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

    # kome je dodeljen ovaj termin, kom frizeru, tj ko ga je napravio
    barber = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self) -> str:
        formatted_date = self.date.strftime('%d-%m-%Y')
        return f"{formatted_date} u {self.time_slot} kod {self.barber}"

    class Meta:
        unique_together = ('date', 'time_slot')
