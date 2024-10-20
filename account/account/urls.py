from drf_spectacular.views import (SpectacularAPIView,
                                   SpectacularRedocView,
                                   SpectacularSwaggerView)
from drf_spectacular.views import SpectacularSwaggerView
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from .views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html')),
    path('api/Accounts/Me', MyUserMeAPIView.as_view()),
    path('api/Accounts/Update', UpdateMeAPIView.as_view()), 
    path('api/Accounts', MyUserAPI.as_view()),
    path('api/Accounts/<int:id>', MyUserByIdAPI.as_view()),
    path('api/Authentication/', include('api.urls')),
    path("api/Doctors", DoctorsAPIView.as_view()),
    path("api/Doctors/<int:id>", DoctorIdAPIView.as_view()),
    # Swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
