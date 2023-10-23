from datetime import date
import re
from django.db import transaction
from rest_framework import serializers
from schedule.models.time_slot import TimeSlot
from schedule.models.working_day import WorkingDay
from schedule.models.schedule import Schedule
from django.contrib.auth import get_user_model
User = get_user_model()

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = "_all__"

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


class WorkingDaySerializerCreate(serializers.ModelSerializer):
    class Meta: 
        model = WorkingDay
        fields = "__all__"

    def validate_date(self, value):
         if value < date.today():
             raise serializers.ValidationError("Datum mora biti danasnji ili unapred")
         return value
    
    # validirati time_slot da ne moze da se unese vreme ako je proslo

    def validate(self, attrs):
        return super().validate(attrs)
    

class SetVacationDaySerializer(serializers.Serializer):
    date = serializers.DateField()
    barber = serializers.IntegerField()

    def validate(self, data):
        existing_working_day = WorkingDay.objects.filter(date=data["date"], barber=data["barber"])
        if existing_working_day:
            raise serializers.ValidationError("Vec ima zakazan slobodan dan za ovog frizera")
        barber = User.objects.get(id=data["barber"])
        WorkingDay.set_vacation(data["date"], barber)
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

