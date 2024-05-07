from http import HTTPStatus

import requests
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from api.base import BaseAPI
from api.methods import delete_user_token_key, get_token_key
from api.serializers.accounts import (
    GoogleAuthSerializer,
    LoginSerializer,
    UserSerializer,
)
from core.exceptions import APIAccessDenied, APIException


class AccountAPI(BaseAPI):
    REQUIRES_AUTH = False

    def list(self, request: Request):
        if request.user.is_anonymous:
            raise APIAccessDenied()

        return Response(
            UserSerializer(
                instance=request.user,
            ).data
        )

    @action(detail=False, methods=["POST"], url_path="register")
    def register(self, request):
        data = LoginSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        try:
            email = data.validated_data.get("email")
            user = User.objects.create_user(email=email, username=email)
            user.set_password(data.validated_data.get("password"))
            user.save()

            return Response(data={"token": get_token_key(user).key})
        except IntegrityError:
            raise APIException(code="user_exist", message="User already exist.")

    @action(detail=False, methods=["POST"], url_path="login")
    def login(self, request):
        data = LoginSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        user = authenticate(
            username=data.validated_data["email"],
            password=data.validated_data["password"],
        )

        if user:
            return Response({"token": get_token_key(user).key})

        raise APIException(
            code="invalid_credential",
            message="Invalid credential.",
        )

    @action(detail=False, methods=["POST"], url_path="google-auth")
    def google_auth(self, request):
        req_data = GoogleAuthSerializer(data=request.data)
        req_data.is_valid(raise_exception=True)

        access_token = req_data.validated_data["access_token"]

        # Get user info
        response = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )
        if response.ok:
            data = response.json()
            email = data["email"]
        else:
            raise ValidationError({"message": "Invalid credential."})

        user, _ = User.objects.get_or_create(username=email)

        return Response({"token": get_token_key(user=user)})

    @action(detail=False, methods=["GET"], url_path="logout")
    def logout(self, request):
        if request.user.is_anonymous:
            raise APIAccessDenied()

        _, _ = delete_user_token_key(request.user, request.auth.key)

        return Response(status=HTTPStatus.NO_CONTENT)
