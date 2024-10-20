


# SECTION - Навигация по микросервису Document



from django.urls import path
from . import views



urlpatterns = [
    path('History/Account/<int:id>', views.HistoryPacientAPIView.as_view()),
    path('History', views.HistoryAPI.as_view()),
    path('History/<int:id>', views.HistoryByIdAPIView.as_view()),
]