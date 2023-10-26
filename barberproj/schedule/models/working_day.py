from django.db import models
from django.contrib.auth import get_user_model
from .time_slot import TimeSlot
from django.core.exceptions import ValidationError
User = get_user_model()

class WorkingDay(models.Model):
    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, null=True, blank=True)

    reserved = models.BooleanField(default=False)

    is_vacation = models.BooleanField(default=False, null=True, blank=True)

    # kome je dodeljen ovaj termin, kom frizeru, tj ko ga je napravio
    barber = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self) -> str:
        formatted_date = self.date.strftime('%d-%m-%Y')
        if self.is_vacation:
            return f"{formatted_date} - Godisnji (Slobodan dan) za {self.barber}"
        return f"{formatted_date} u {self.time_slot} kod {self.barber}"

    class Meta:
        unique_together = ('date', 'time_slot')

    
    @classmethod
    def set_vacation(cls, date, barber):
        new_working_day_as_vacation = cls(
            date=date,
            barber=barber,
            is_vacation=True,
            time_slot=None
        )
        new_working_day_as_vacation.save()

    # def save(self, *args, **kwargs):
    #     if self.is_vacation:
    #         # raise ValidationError("Time slot should be None for vacation days.")
    #         self.time_slot = W
    #     # else:
    #     #     raise Exception
    #     super().save(*args, **kwargs)
