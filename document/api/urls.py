from django.urls import path
from . import views

urlpatterns = [
    path('History/Account/<int:id>/', views.HistoryPacientAPIView.as_view()),
    path('History/', views.HistoryAPIView.as_view()),
    path('History/<int:id>/', views.HistoryAPIView.as_view()),
]