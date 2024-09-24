from django.urls import path
from .views import SignUpAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('SignUp/', SignUpAPIView.as_view()),
    path('SignIn/', TokenObtainPairView.as_view())
]