from rest_framework import serializers

from decks.models import Deck


class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ["id", "name", "visibility"]

    def create(self, validated_data):
        return Deck.objects.create(
            user=self.context["user"],
            **validated_data,
        )
