# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from django.conf import settings

from oauth2_provider.models import Application, AccessToken
from oauth2_provider.contrib.rest_framework import TokenHasScope, OAuth2Authentication
from oauth2_provider.views.generic import ProtectedResourceMixin
from users.models import User
from users.serializers import AccessTokenSerializer, RegisterSerializer, UserSerializer


class UserDetailView(APIView, ProtectedResourceMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


# class ApiEndpoint(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request, *args, **kwargs):

#         # Application.objects.all().delete()

#         Application.objects.create(
#             name="NestJS App",
#             client_id="uhdonKnGrDtOJP6OkwoGSz49jLvb7CqSno6VlmYv",
#             client_secret="QsAOpfYmXGxqUc46jJFjh81rZRCYwKTbmUjK1aoUuxeMMn3rdJvd92S2tvs919LrtTIHA7EUzmyDtxmx3l1fE8Tv07q3XFUPMx0eTvhUHM5DSsKXiCfSI3Pa6VGnzabc",
#             client_type=Application.CLIENT_CONFIDENTIAL,
#             authorization_grant_type=Application.GRANT_PASSWORD,
#         )

#         print("a")
#         return Response("Hello, OAuth2!")


class RegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Registered successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )


from django.contrib.auth import authenticate, login
from oauth2_provider.oauth2_backends import get_oauthlib_core
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from oauth2_provider.models import AccessToken, Application, RefreshToken
from django.core.cache import cache


class RequestAuthorizationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            # Lưu thông tin đăng nhập tạm thời vào session

            login(request, user)
            cache.set(
                f"auth_{username}",
                {"username": username, "password": password},
                timeout=300,
            )

            return Response(
                {"message": "Authorization requested. Please approve or deny."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


class ApproveAuthorizationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        client_id = request.data.get("client_id")
        username = request.data.get("username")
        credentials = cache.get(f"auth_{username}")
        print(credentials)

        # client_id = "uhdonKnGrDtOJP6OkwoGSz49jLvb7CqSno6VlmYv"
        if credentials:
            user = authenticate(
                username=credentials["username"], password=credentials["password"]
            )

            if user:
                application = get_object_or_404(Application, client_id=client_id)
                token = AccessToken.objects.create(
                    user=user,
                    application=application,
                    expires=timezone.now() + timedelta(days=1),
                    token=generate_token(),
                    scope="read",
                )
                RefreshToken.objects.create(
                    user=user,
                    application=application,
                    token=generate_token(),
                    access_token=token,
                )
                cache.delete(f"auth_{username}")

                return Response(
                    {
                        "access_token": token.token,
                        "expires_in": settings.OAUTH2_PROVIDER[
                            "ACCESS_TOKEN_EXPIRE_SECONDS"
                        ],
                        "token_type": "Bearer",
                        "scope": token.scope,
                    }
                )
        return Response(
            {"error": "Không được cấp quyền"}, status=status.HTTP_403_FORBIDDEN
        )


class DenyAuthorizationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        credentials = cache.get(f"auth_{username}")
        if credentials:
            # Xóa thông tin đăng nhập tạm thời khỏi cache
            cache.delete(f"auth_{username}")
            return Response({"message": "Từ chối truy cập."})

        return Response(
            {"error": "Không được cấp quyền"}, status=status.HTTP_403_FORBIDDEN
        )


def generate_token():
    import uuid

    return str(uuid.uuid4())
