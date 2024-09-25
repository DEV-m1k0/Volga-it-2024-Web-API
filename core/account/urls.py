from django.urls import path, include
from account.views import MyUserIdAPIView, MyUserAPIView, MyUserMeAPIView, UpdateMeAPIView
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('Me/', MyUserMeAPIView.as_view()),
    path("Update/", UpdateMeAPIView.as_view()),
    path('<int:id>/', MyUserIdAPIView.as_view()),
    path('', MyUserAPIView.as_view()),
]