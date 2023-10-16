from datetime import datetime
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from schedule.models.working_day import WorkingDay
from api.serializers.serializers_shedule import ScheduleSerializer, ScheduleSerializerCreate, WorkingDaySerializer, WorkingDaySerializerCreate
from barberProfile.admin import User
from schedule.models.schedule import Schedule
from datetime import date
from rest_framework import serializers


class ScheduleListByBarber(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # user = self.request.user
        return Schedule.objects.filter(barber=4)


class WorkingDayByDate(generics.ListAPIView):
    serializer_class = WorkingDaySerializer

    def get_queryset(self):
        date_param = self.kwargs.get("date")
        if date_param: 
            date_param = date.fromisoformat(date_param)
            if date_param < date.today():
                raise serializers.ValidationError("Date must be equal to or greater than today's date.")
            return WorkingDay.objects.filter(date=date_param)


class CreateWorkingDay(APIView):
    # permission_classes = (IsAuthenticated, )

    @transaction.atomic
    def post(self, request):
        data = request.data  # Assuming request.data is a list of objects
        created_working_days = []

        for item in data:
            serializer = WorkingDaySerializerCreate(data=item)
            if serializer.is_valid():
                serializer.save()
                created_working_days.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(created_working_days, status=status.HTTP_201_CREATED)
    

class CreateSchedule(APIView):
    @transaction.atomic
    def post(self, request):
         print(request.data)
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