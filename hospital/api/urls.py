


# SECTION - URL's для микросервиса Hospital



from django.urls import path
from .views import *



urlpatterns = [
    path('Hospitals', HospitalsAPIView.as_view()),
    path('Hospitals/<int:id>', HospitalByIdAPIView.as_view()),
    path('Hospitals/<int:id>/Rooms', RoomsByIdAPIView.as_view())
]