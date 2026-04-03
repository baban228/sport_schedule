from django.urls import path
from .views import MyScheduleView

urlpatterns = [
    path('my-schedule/', MyScheduleView.as_view()),
]