from rest_framework.views import APIView
from .logic import history

# Create your views here.

class HistoryAPIView(APIView):
    def post(self, request):

        response = history.post_history(request)

        return response