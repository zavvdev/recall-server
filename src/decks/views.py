from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class DeckListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pass

    def post(self, request):
        pass

    def delete(self, request):
        pass


class DeckDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        pass

    def put(self, request, id):
        pass

    def patch(self, request, id):
        pass

    def delete(self, request, id):
        pass
