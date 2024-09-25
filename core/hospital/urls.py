from django.urls import path
from .views import HospitalsAPIView, RoomsByIdAPIVIew

urlpatterns = [
    path('', HospitalsAPIView.as_view()),
    path('<int:id>/', HospitalsAPIView.as_view()),
    path('<int:id>/Rooms/', RoomsByIdAPIVIew.as_view())
]