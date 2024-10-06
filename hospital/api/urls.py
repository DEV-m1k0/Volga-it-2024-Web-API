from django.urls import path
from .views import HospitalsAPIView, RoomsByIdAPIView

urlpatterns = [
    path('Hospitals/', HospitalsAPIView.as_view()),
    path('Hospitals/<int:id>/', HospitalsAPIView.as_view()),
    path('Hospitals/<int:id>/Rooms/', RoomsByIdAPIView.as_view())
]