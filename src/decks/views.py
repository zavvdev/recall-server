from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from decks.serializers import DeckSerializer
from shared.responses import api_response


class DeckListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pass

    def post(self, request):
        serializer = DeckSerializer(
            data=request.data,
            context={"user": request.user},
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return api_response(
            status=status.HTTP_201_CREATED,
        )

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
