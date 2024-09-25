from django.urls import path
from .views import HospitalsAPIView


urlpatterns = [
    path('', HospitalsAPIView.as_view()),
]