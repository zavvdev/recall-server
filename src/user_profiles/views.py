from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from shared.responses import api_response

from .serializers import UserProfileSerializer


class UserProfileView(APIView):
    # Reject unauthenticated requests.
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        # Pass profile model into serializer. This type of mode is
        # read-only mode since we only extract fields from profile.
        serializer = UserProfileSerializer(profile)
        return api_response(
            data=serializer.data,
        )

    def patch(self, request):
        profile = request.user.profile
        # Since we linked our UserProfile model to serializer, when we
        # pass data into it, it makes serializer to run in write/update
        # mode and automatically call either create or update method
        # that are inherited from ModelSerializer.
        # In this case, it calls update method because we passed profile
        # model in first argument, so it will be updated with provided data.
        # All validation rules are pulled from UserProfile model since we
        # linked it to serializer.
        serializer = UserProfileSerializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        # Update method is called here which updates profile model with
        # provided data automatically.
        serializer.save()
        return api_response()
