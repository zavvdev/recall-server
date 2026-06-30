from django.urls import path

from shared.url_names import UrlName

from .views import DeckDetailView, DeckListView

urlpatterns = [
    path("", DeckListView.as_view(), name=UrlName.DECK_LIST),
    path("<int:id>/", DeckDetailView.as_view(), name=UrlName.DECK_DETAIL),
]
