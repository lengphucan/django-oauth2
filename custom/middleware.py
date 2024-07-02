# middleware.py

from django.http import JsonResponse
from oauth2_provider.models import AccessToken
from oauth2_provider.settings import oauth2_settings
from django.utils.deprecation import MiddlewareMixin
import datetime


class OAuth2TokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", None)
        if auth_header:
            try:
                token_type, access_token = auth_header.split(" ")
                if token_type.lower() == "bearer":
                    token = AccessToken.objects.get(token=access_token)
                    if token.is_valid():  # and token.expires > datetime.datetime.now():
                        request.user = token.user
                        request.auth = token
                    else:
                        return JsonResponse(
                            {"error": "Token has expired or is invalid."}, status=401
                        )
            except AccessToken.DoesNotExist:
                return JsonResponse({"error": "Token does not exist."}, status=401)
            except ValueError:
                return JsonResponse({"error": "Invalid token format."}, status=401)
        else:
            return JsonResponse({"error": "Authorization header missing."}, status=401)
