from django.urls import path
from . import views

urlpatterns = [
    path('History/', views.HistoryAPIView.as_view())
]