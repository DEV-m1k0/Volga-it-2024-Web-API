from django.urls import path
from .views import SignUpAPIView


urlpatterns = [
    path('SignUp/', SignUpAPIView.as_view())
]