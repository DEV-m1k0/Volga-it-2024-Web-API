from django.urls import path
from .views import (TimeTableAPIView, TimeTableByDoctorAPIVIew, 
                    TimeTableByHospitalAPIView, TimeTableByRoomAPIView)


urlpatterns = [
    path('Timetable/', TimeTableAPIView.as_view()),
    path("Timetable/<int:id>/", TimeTableAPIView.as_view()),
    path("Timetable/Doctor/<int:id>/", TimeTableByDoctorAPIVIew.as_view()),
    path("Timetable/Hospital/<int:id>/", TimeTableByHospitalAPIView.as_view()),
    path("Timetable/Hospital/<int:id>/Room/<str:room>/", TimeTableByRoomAPIView.as_view())
]
