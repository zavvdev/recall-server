from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from cards.serializers import CardSerializer
from shared.messages import Messages
from shared.responses import api_response


class CardListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            deck = request.user.decks.get(pk=request.data["deck"])
        except request.user.decks.model.DoesNotExist:
            return api_response(
                message=Messages.DECK_NOT_FOUND,
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer.save(deck=deck)
        return api_response(
            status=status.HTTP_201_CREATED,
        )
