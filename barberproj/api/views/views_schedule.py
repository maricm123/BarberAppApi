from datetime import datetime
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from schedule.models.time_slot import TimeSlot
from schedule.models.working_day import WorkingDay
from api.serializers.serializers_shedule import GetTimeSlotSerializer, ScheduleSerializer, ScheduleSerializerCreate, SetVacationDaySerializer, TimeSlotSerializer, WorkingDaySerializer, WorkingDaySerializerCreate
from barberProfile.admin import User
from schedule.models.schedule import Schedule
from datetime import date
from rest_framework import serializers

"""WORKING DAY VIEWS"""


class WorkingDayByDate(generics.ListAPIView):
    """
    This endpoint retrieves a list of time .

    - Request method: GET
    - URL: /api/day/YYYY-MM-DD
    """
    serializer_class = WorkingDaySerializer

    def get_queryset(self):
        date_param = self.kwargs.get("date")
        if date_param: 
            date_param = date.fromisoformat(date_param)
            if date_param < date.today():
                raise serializers.ValidationError("Date must be equal to or greater than today's date.")
            return WorkingDay.objects.filter(date=date_param)


class CreateWorkingDay(APIView):
    permission_classes = (IsAuthenticated, )

    @transaction.atomic
    def post(self, request):
        user = request.user
        data = request.data  # Convert request.data to a list
        for entry in data:
            entry["barber"] = user.id

        # Create a list of WorkingDaySerializerCreate instances
        serializers = [WorkingDaySerializerCreate(data=item) for item in data]

        # Check if all serializers are valid
        is_valid = all(serializer.is_valid() for serializer in serializers)

        if is_valid:
            created_slots_in_working_days = []
            for serializer in serializers:
                serializer.save()
                created_slots_in_working_days.append(serializer.data)
            return Response(created_slots_in_working_days, status=status.HTTP_201_CREATED)
        else:
            # If any serializer is invalid, return the errors
            errors = [serializer.errors for serializer in serializers if not serializer.is_valid()]
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class SetVacationWorkingDay(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = SetVacationDaySerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class DeletePastWorkingDays(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, )

    @transaction.atomic
    def delete(self, request):
        past_working_days = WorkingDay.objects.filter(date__lt=datetime.today())
        past_working_days.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    

class DeleteWorkingDayTimeSlot(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, )

    @transaction.atomic
    def delete(self, request, pk):
        working_day_time_slot = WorkingDay.objects.get(id=pk)
        try:
            working_day_time_slot.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)


"""SCHEDULE VIEWS"""


class ScheduleListByBarber(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        date_param = self.kwargs.get("date")
        if date_param: 
            date_param = date.fromisoformat(date_param)
            if date_param < date.today():
                raise serializers.ValidationError("Date must be equal to or greater than today's date.")
            return Schedule.objects.filter(date_time__barber=user, date_time__date=date_param)


class CreateSchedule(APIView):
    @transaction.atomic
    def post(self, request):
         serializer = ScheduleSerializerCreate(data=request.data)
         serializer.is_valid(raise_exception=True)
         return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteSchedule(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, )

    @transaction.atomic
    def delete(self, request, pk):
        schedule = Schedule.objects.get(id=pk)
        try:
            working_day = schedule.date_time
            working_day.reserved = False
            working_day.save(update_fields=['reserved'])
            schedule.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)


class GetAllTimeSlots(generics.ListAPIView):
    """
    This endpoint retrieves a list of time slots.
    """
    serializer_class = GetTimeSlotSerializer

    def get_queryset(self):
        return TimeSlot.objects.all()
    

