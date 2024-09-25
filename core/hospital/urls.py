from django.urls import path
from .views import HospitalsAPIView


urlpatterns = [
    path('', HospitalsAPIView.as_view()),
    path('<int:id>/', HospitalsAPIView.as_view())
]