from django.contrib import admin
from django.contrib.auth import get_user_model
from .models.working_day import WorkingDay
from .models.schedule import Schedule
from .models.time_slot import TimeSlot


class WorkingDayAdmin(admin.ModelAdmin):
    list_display = ('date', 'time_slot', 'shift', 'reserved')
    ordering = ('date',)  # This specifies the default ordering by date in ascending order

admin.site.register(Schedule)
admin.site.register(WorkingDay)
admin.site.register(TimeSlot)