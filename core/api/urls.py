from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView



urlpatterns = [
    path('', include('rest_framework.urls')),
    path('Accounts/', include('account.urls')),
    path('Authentication/', include('authentication.urls'))
]