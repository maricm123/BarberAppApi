from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import include, path
from api.views import views_schedule, views_barber, views_browsable
from django.conf import settings


app_name = "core"


endpoints_urlpatterns = [
    # SCHEDULES
    path('schedules-by-me/', views_schedule.ScheduleListByBarber.as_view(), name='schedules-by-me'),
    path('create-schedule/', views_schedule.CreateSchedule.as_view(), name='create-schedule'),
    path('delete-schedule/<int:pk>/', views_schedule.DeleteSchedule.as_view(), name='delete-schedule'),
    # WORKING DAY
    path('day/<str:date>/', views_schedule.WorkingDayByDate.as_view(), name='day'),
    path('create-day/', views_schedule.CreateWorkingDay.as_view(), name='create-day'),
    path('delete-past-working-days/', views_schedule.DeletePastWorkingDays.as_view(), name='delete-past-working-days'),
    path('set-vacation/', views_schedule.SetVacationWorkingDay.as_view(), name='set-vacation'),
    # AUTHENTICATION
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('barber-login/', views_barber.UserLoginView.as_view(), name='user-login'),
    path('barber-register/', views_barber.UserRegisterView.as_view(), name='coach-register'),
    path('current-user/', views_barber.CurrentUserView.as_view(),
             name='current-user'),
]


urlpatterns = [path("", include(endpoints_urlpatterns))]


if settings.DEBUG:
    endpoints_urlpatterns_debug = [
        path(route="", view=views_browsable.APIRootView.as_view(), name="root"),
    ]
    urlpatterns += [path("", include(endpoints_urlpatterns_debug))]
