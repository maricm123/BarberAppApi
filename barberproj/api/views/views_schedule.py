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
from api.serializers.serializers_shedule import ScheduleSerializer, WorkingDaySerializer, WorkingDaySerializerCreate
from barberProfile.admin import User
from schedule.models.schedule import Schedule

class ScheduleListByBarber(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # user = self.request.user
        return Schedule.objects.filter(barber=4)
    
from datetime import date
from rest_framework import serializers

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
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = WorkingDaySerializerCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=HTTP_201_CREATED)



    