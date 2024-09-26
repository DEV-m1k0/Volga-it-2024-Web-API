from django.urls import path, include
from .views import TimeTableAPIView, TimeTableByDoctorAPIVIew


urlpatterns = [
    path('', TimeTableAPIView.as_view()),
    path("<int:id>/", TimeTableAPIView.as_view()),
    path("Doctor/<int:id>/", TimeTableByDoctorAPIVIew.as_view())
]
