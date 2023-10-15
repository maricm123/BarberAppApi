from rest_framework import serializers
from schedule.models.time_slot import TimeSlot
from schedule.models.working_day import WorkingDay
from schedule.models.schedule import Schedule


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
        model = Schedule
        fields = "__all__"
