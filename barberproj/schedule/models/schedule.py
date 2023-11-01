from django.db import models
from django.contrib.auth import get_user_model

from config.tasks import send_mail_for_schedule
# from api.mixins import send_mail_for_schedule
from .working_day import WorkingDay
from django.db import transaction

User = get_user_model()

class Schedule(models.Model):
    customer = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    # ovde nam ne treba barber, jer ga imamo u working day
    # kada prikazujemo od barbera zakazivanja, filtriramo wokring day sa reserved = True
    # i tako dobijamo zakazane termine za frizera.
    # barber = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.ForeignKey(WorkingDay, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer} u: {self.date_time}" 

    @classmethod
    def create(cls, customer, telephone, email, date_time):
        try:
            schedule_obj = cls(
                customer=customer,
                telephone=telephone,
                email=email,
                # barber=barber,
                date_time=date_time
            )
            schedule_obj.save()
            barber = date_time.barber
            print(barber.name)
            time = date_time.time_slot
            date = date_time.date
            formatted_date = date.strftime('%d-%m-%Y')
            try:
                print("PRE SLANJA MJELA")
                send_mail_for_schedule.delay(email=email, barber=barber.name, time=time.start, date=formatted_date)
                print("SENDED MAIL")
            except Exception as e:
                print("SLANJE MEJLA ERROR U SCHEDULE", e)
        except Exception as e:
            print(e, "CREATESCHEDUE ERROR")
