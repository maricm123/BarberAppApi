from datetime import date
import re
from django.db import transaction
from rest_framework import serializers
from api.mixins import ReqContextMixin
from schedule.models.time_slot import TimeSlot
from schedule.models.working_day import WorkingDay
from schedule.models.schedule import Schedule
from django.contrib.auth import get_user_model
from datetime import datetime, time

User = get_user_model()

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = "__all__"


class GetTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ["id", "start",]


class WorkingDaySerializer(serializers.ModelSerializer):
    time_slot = TimeSlotSerializer()

    class Meta:
        model = WorkingDay
        fields = "__all__"


class ScheduleSerializer(serializers.ModelSerializer):
    date_time = WorkingDaySerializer()

    class Meta:
        model = Schedule
        fields = "__all__"


# U ovaj serializer ulazi za svaki objekat po jednom, tako da ne treba da koristim for loop.
class WorkingDaySerializerCreate(serializers.ModelSerializer):
    class Meta: 
        model = WorkingDay
        fields = "__all__"

    def validate_date(self, value):
         if value < date.today():
             raise serializers.ValidationError("Datum mora biti danasnji ili unapred")
         return value

    # ovde validiramo : prvo gledamo ako je danasnji datum onda gledamo time_slotove koje smo ubacili 
    # ako datum nije danasnji onda mora biti neki unapred, sto znaci da time_slot moze biti koji god!
    def validate(self, data):
        # trenutno vreme (ne datum samo vreme)
        current_time = datetime.now().time()
        time_slot = data["time_slot"]

        # konvertovan string time slot u pravo vreme
        time_slot_real_time = time.fromisoformat(time_slot.start)

        # vracamo gresku samo ako je datum danasnji
        if datetime.today().date() == data["date"]:
            # i ako je sadasnje vreme vece od time_slot vremena koje frizer ubacuje
            if current_time > time_slot_real_time:
                raise serializers.ValidationError("Termin koji ubacujes je prosao za danasnji dan.")

        return data
    

class SetVacationDaySerializer(ReqContextMixin, serializers.Serializer):
    date = serializers.DateField()

    def validate_date(self, value):
         if value < date.today():
             raise serializers.ValidationError("Datum mora biti danasnji ili unapred")
         return value

    def validate(self, data):
        existing_working_day = WorkingDay.objects.filter(date=data["date"], barber=self._req_context.user)
        if existing_working_day:
            raise serializers.ValidationError("Vec ima zakazanih termina za ovog frizera za ovaj datum")
        WorkingDay.set_vacation(data["date"], self._req_context.user)
        return data


class RemoveVacationDaySerializer(ReqContextMixin, serializers.Serializer):
    date = serializers.DateField()

    def validate_date(self, value):
         if value < date.today():
             raise serializers.ValidationError("Datum mora biti danasnji ili unapred")
         return value

    def validate(self, data):
        try:
            WorkingDay.remove_vacation(data["date"], self._req_context.user)
        except Exception as e:
            raise serializers.ValidationError("Taj datum nije setovan prethodno kao slobodan dan.")
        return data


class ScheduleSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"

    def validate_date_time(self, value):
        if value.reserved:
            raise serializers.ValidationError("Ovaj termin je vec zakazan")
        if value.is_vacation:
            raise serializers.ValidationError("Danas je slobodan dan, ne mozete rezervisati termin")
        return value

    def validate_email(self, value):
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', value):
            raise serializers.ValidationError("Pogresan format emaila.")
        return value

    def validate_telephone(self, value):
        if not re.match(r'^[0-9]{7,}$', value):
            raise serializers.ValidationError("Pogresan format telefonskog broja")
        return value

    def validate(self, data):
        working_day = data["date_time"]
        try:
            with transaction.atomic():
                working_day.reserved = True
                working_day.save(update_fields=['reserved'])
                Schedule.create(**data)
        except Exception as e:
            raise serializers.ValidationError("Greska prilikom kreiranja rezervacije.")
        return data
