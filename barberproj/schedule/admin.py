from django.contrib import admin
from django.contrib.auth import get_user_model
from .models.working_day import WorkingDay
from .models.schedule import Schedule
from .models.time_slot import TimeSlot

User = get_user_model()

admin.site.register(Schedule)
admin.site.register(WorkingDay)
admin.site.register(TimeSlot)