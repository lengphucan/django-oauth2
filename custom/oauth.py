from oauth2_provider.backends import OAuth2Backend

from django.contrib.auth import get_user_model

# from users.models import User

User = get_user_model()


class CustomOAuth2Backend(OAuth2Backend):
    def authenticate(self, request, **credentials):
        # print(User.objects.all())
        username_or_email = credentials.get("username")
        password = credentials.get("password")
        if username_or_email is None or password is None:
            return None

        try:
            # Try to fetch the user by email or username
            user = User.objects.get(email=username_or_email) or User.objects.get(
                username=username_or_email
            )
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None
