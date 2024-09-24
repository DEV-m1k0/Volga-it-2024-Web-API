from django.urls import path, include
from account.views import MyUserViewSet, MyUserAPIView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', MyUserViewSet)


urlpatterns = [
    path('', MyUserAPIView.as_view()),
    path('', include(router.urls)),
]