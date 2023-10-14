from django.db import models
from django.contrib.auth import get_user_model
from .working_day import WorkingDay

User = get_user_model()

class Schedule(models.Model):
    customer = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    barber = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.ForeignKey(WorkingDay, on_delete=models.CASCADE)
    # schedule_date = models.DateField()
    # schedule_time = models.TimeField()

    def __str__(self):
        return f"{self.customer} with {self.barber} at {self.date_time}"