from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import include, path
from api.views import views_schedule, views_barber
app_name = "api"

urlpatterns = [
    # SCHEDULES
    path('schedules-by-me/', views_schedule.ScheduleListByBarber.as_view(), name='schedules-by-me'),
    path('create-schedule/', views_schedule.CreateSchedule.as_view(), name='create-schedule'),
    path('delete-schedule/<int:pk>/', views_schedule.DeleteSchedule.as_view(), name='delete-schedule'),
    # WORKING DAY
    path('day/<str:date>/', views_schedule.WorkingDayByDate.as_view(), name='day'),
    path('create-day/', views_schedule.CreateWorkingDay.as_view(), name='create-day'),
    # AUTHENTICATION
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('barber-login/', views_barber.UserLoginView.as_view(), name='user-login'),
    path('barber-register/', views_barber.UserRegisterView.as_view(), name='coach-register'),
    path('current-user/', views_barber.CurrentUserView.as_view(),
             name='current-user'),
]
