from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView as JwtTokenRefreshView

from shared.messages import Messages
from shared.responses import api_response

from .serializers import LoginSerializer


class TokenRefreshView(JwtTokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return api_response(message=Messages.OK, data=response.data, status=response.status_code)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Calling Django's authenticate(). This loops through AUTHENTICATION_BACKENDS,
        # hits our AuthWithEmailOrUsernameBackend, and returns either a User
        # instance or None.
        user = authenticate(
            request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if user is None:
            return api_response(
                Messages.AUTH_INVALID_CREDENTIALS, data=None, status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)
        return api_response(
            Messages.AUTH_LOGIN_SUCCESS,
            data={
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
        )
