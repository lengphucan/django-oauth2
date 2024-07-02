import re
from oauth2_provider.models import Application, AccessToken
from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth import authenticate


from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "balance"]


class AccessTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessToken
        fields = "__all__"


from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.core.exceptions import ValidationError


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "username"]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "referer": {
                "write_only": True,
            },
            "username": {"max_length": 20},
        }

    def validate_email(self, value):
        return value.lower()

    def validate_username(self, value):
        pattern = r"^[a-zA-Z0-9]+$"
        if not re.match(pattern, value):
            raise ValidationError("Chỉ cho phép sử dụng (a-z), (0-9).")
        return value

    def create(self, validated_data):
        user = User(**validated_data)
        user.save()
        return user


# class UserLoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

#     def validate(self, data):
#         username_or_email = data.get("username")
#         password = data.get("password")

#         if username_or_email and password:
#             user = self.authenticate(username_or_email, password)
#             if user:
#                 if user.is_active:
#                     return user
#                 else:
#                     raise serializers.ValidationError("User is deactivated")
#             else:
#                 raise serializers.ValidationError(
#                     "Invalid username or email or password"
#                 )
#         else:
#             raise serializers.ValidationError(
#                 'Must include "username_or_email" and "password"'
#             )

#     def authenticate(self, username_or_email, password):
#         user = (
#             User.objects.filter(email=username_or_email).first()
#             or User.objects.filter(username=username_or_email).first()
#         )
#         if user:
#             if user.check_password(password):
#                 return user
#         return None
