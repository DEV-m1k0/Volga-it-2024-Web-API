from django.urls import path, include
from account.views import MyUserViewSet, MyUserAPIView, MyUserMeAPIView, UpdateMeAPIView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', MyUserViewSet)


urlpatterns = [
    path('Me/', MyUserMeAPIView.as_view()),
    path("Update/", UpdateMeAPIView.as_view()),
    path('', MyUserAPIView.as_view()),
    path('', include(router.urls)),
]