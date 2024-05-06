import uuid

from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed

from api.models import TokenKey

SENSITIVE_ATTRIBUTES = [
    "key",
    "access_token",
    "password",
    "token",
]


def clean_sensitive_data(data):
    for key, value in data.items():
        if key in SENSITIVE_ATTRIBUTES:
            data[key] = "****"

    return data


def generate_token_key(rounds=2) -> str:
    return "".join(str(uuid.uuid4()).replace("-", "") for _ in range(rounds))


def get_token_key(user: User) -> TokenKey:
    key, _ = TokenKey.objects.get_or_create(
        user=user, defaults={"key": generate_token_key()}
    )
    return key


def get_user_by_token(token_key: str = None):
    if not token_key:
        return None

    token_key = token_key.split(" ")
    if len(token_key) != 2:
        return None

    try:
        token_key = TokenKey.objects.prefetch_related("user").get(
            key=token_key[1], is_active=True
        )
        user = token_key.user
    except TokenKey.DoesNotExist:
        raise AuthenticationFailed(code="invalid_token_key", detail="Invalid Token Key")

    return user, token_key


def delete_user_token_key(user: User, token_key: str) -> tuple[int, dict]:
    return TokenKey.objects.get(user=user, key=token_key).delete()
