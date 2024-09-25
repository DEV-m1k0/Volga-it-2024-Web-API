from django.urls import path, include
from .views import DoctorsAPIView


urlpatterns = [
    path('', include('rest_framework.urls')),
    path('Accounts/', include('account.urls')),
    path('Authentication/', include('authentication.urls')),
    path("Doctors/", DoctorsAPIView.as_view())
]