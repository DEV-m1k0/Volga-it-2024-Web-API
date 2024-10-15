from django.urls import path
from .views import (TimeTableAPIView, TimeTableByDoctorAPIVIew, 
                    TimeTableByHospitalAPIView, TimeTableByRoomAPIView,
                    AppointmentsByTimetableAPIView, DeleteAppointmentByIdAPIView)


urlpatterns = [
    path('Timetable/', TimeTableAPIView.as_view()),
    path("Timetable/<int:id>/", TimeTableAPIView.as_view()),
    path("Timetable/Doctor/<int:id>/", TimeTableByDoctorAPIVIew.as_view()),
    path("Timetable/Hospital/<int:id>/", TimeTableByHospitalAPIView.as_view()),
    path("Timetable/Hospital/<int:id>/Room/<str:room>/", TimeTableByRoomAPIView.as_view()),
    path("Timetable/<int:id>/Appointments/", AppointmentsByTimetableAPIView.as_view()),
    path("Timetable/Appointments/<int:id>/", DeleteAppointmentByIdAPIView.as_view())
]
