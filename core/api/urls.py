from django.urls import path, include



urlpatterns = [
    path('', include('rest_framework.urls')),
    path('Accounts/', include('account.urls')),
    path('Authentication/', include('authentication.urls'))
]