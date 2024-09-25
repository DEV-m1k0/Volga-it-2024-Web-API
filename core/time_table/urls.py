from django.urls import path, include
from .views import TimeTableAPIView


urlpatterns = [
    path('', TimeTableAPIView.as_view())
]
