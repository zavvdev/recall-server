from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from cards.serializers import CardSerializer
from decks.serializers import DeckSerializer
from shared.messages import Messages
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
        deck_object = serializer.save(user=request.user)
        serialized_deck = DeckSerializer(deck_object)
        return api_response(
            status=status.HTTP_201_CREATED, data=serialized_deck.data
        )

    def delete(self, request):
        request.user.decks.all().delete()
        return api_response()


class DeckDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            deck = request.user.decks.get(pk=pk)
            serializer = DeckSerializer(deck)
            return api_response(data=serializer.data)
        except request.user.decks.model.DoesNotExist:
            return api_response(
                message=Messages.NOT_FOUND, status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, pk):
        try:
            deck = request.user.decks.get(pk=pk)
            serializer = DeckSerializer(deck, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return api_response()
        except request.user.decks.model.DoesNotExist:
            return api_response(
                message=Messages.NOT_FOUND, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            deck = request.user.decks.get(pk=pk)
            deck.delete()
            return api_response()
        except request.user.decks.model.DoesNotExist:
            return api_response(
                message=Messages.NOT_FOUND, status=status.HTTP_404_NOT_FOUND
            )


class DeckCardsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            deck = request.user.decks.get(pk=pk)
            cards = deck.cards.all()
            serializer = CardSerializer(cards, many=True)
            return api_response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        except request.user.decks.model.DoesNotExist:
            return api_response(
                message=Messages.DECK_NOT_FOUND,
                status=status.HTTP_404_NOT_FOUND,
            )
