from datetime import date
from rest_framework import serializers
from schedule.models.time_slot import TimeSlot
from schedule.models.working_day import WorkingDay
from schedule.models.schedule import Schedule
from django.contrib.auth import get_user_model
User = get_user_model()

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = "__all__"


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


class ScheduleSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"

    # def validate_barber(self, value):
    #     print(value.id)
    #     try:
    #         barber = User.objects.get(id=value)
    #     except User.DoesNotExist:
    #         raise serializers.ValidationError("Slot does not exist")
            
    # def validate_date_time(self, value):
    #     print(value.id)
    #     try:
    #         date_time = WorkingDay.objects.get(id=value)
    #     except WorkingDay.DoesNotExist:
    #         raise serializers.ValidationError("Slot does not exist")
    #     return value.id

    def validate(self, data):
        Schedule.create(**data)
        working_day = data["date_time"]
        working_day.reserved = True
        working_day.save(update_fields=['reserved'])
        return data

