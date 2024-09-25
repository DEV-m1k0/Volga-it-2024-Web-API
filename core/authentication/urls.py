from django.urls import path
from .views import SignUpAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import ResetTokenAPIView, ValidateTokenAPIView
from django.contrib.auth import authenticate



urlpatterns = [
    path('SignUp/', SignUpAPIView.as_view()),
    path('SignIn/', TokenObtainPairView.as_view()),
    path('SignOut/', ResetTokenAPIView.as_view()),
    path('Validate/', ValidateTokenAPIView.as_view()),
    path('Refresh/', TokenRefreshView.as_view())
]