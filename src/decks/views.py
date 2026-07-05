from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from decks.serializers import DeckSerializer
from shared.responses import api_response


class DeckListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        decks = request.user.decks.all()
        # manu=True - serialize a list of decks
        # instead of one.
        serializer = DeckSerializer(decks, many=True)
        return api_response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = DeckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return api_response(
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request):
        request.user.decks.all().delete()
        return api_response()


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
