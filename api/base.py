import logging
import traceback

from django.conf import settings
from django.utils.timezone import now
from rest_framework import response, viewsets
from rest_framework.authentication import BaseAuthentication

from api.methods import clean_sensitive_data, get_user_by_token
from api.models import TokenKey
from core.exceptions import (
    APIAccessDenied,
    APIConflict,
    APIException,
    APIForbidden,
    APINotFound,
)

log = logging.getLogger(__name__)


class TokenKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token_key = request.META.get("HTTP_AUTHORIZATION")
        if token_key:
            return get_user_by_token(token_key=token_key)
        return None


class BaseAPI(viewsets.GenericViewSet):
    ADMIN_ONLY = False
    REQUIRES_AUTH = True

    authentication_classes = [TokenKeyAuthentication]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _check_auth(self, request):
        if request.user.is_authenticated:
            TokenKey.objects.filter(key=request.auth.key).update(last_used=now())

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        # Check if the request contains a Bearer token
        self._check_auth(request)
        if self.REQUIRES_AUTH:
            self.auth_required(request=request)

    def admin_only(self, request):
        if (
            not request.user
            or not request.user.is_authenticated
            or not request.user.is_superuser
        ):
            raise APIAccessDenied()

    def auth_required(self, request):
        if not self.request.user or not self.request.user.is_authenticated:
            raise APIAccessDenied()

    def _get_clean_data(self):
        get_data = dict(self.request.GET)
        data = self.request.data
        post_data = None

        # Don't log sensitive data
        # Checking whether it's bulk insert or not
        if isinstance(data, list):
            post_data = []
            for d in data:
                raw_post_data = dict(d)
                post_data.append(clean_sensitive_data(raw_post_data))
        if self.request.data:
            raw_post_data = dict(self.request.data)
            post_data = clean_sensitive_data(raw_post_data)

        get_data = clean_sensitive_data(get_data)
        return get_data, post_data

    def finalize_response(self, request, response, *args, **kwargs):
        if settings.DEBUG:
            get_data, post_data = self._get_clean_data()
            logging.info(
                "DEBUG API call api=%s method=%s path=%s query=%s post_data=%s",
                self.get_view_name(),
                self.request.method,
                self.request.path,
                get_data,
                post_data,
            )
        return super().finalize_response(request, response, *args, **kwargs)

    def handle_exception(self, exc):
        tb = traceback.TracebackException.from_exception(exc)
        get_data, post_data = self._get_clean_data()

        logging.error(
            "Exception=%s api=%s method=%s user=%s data=%s path=%s query=%s",
            "".join(tb.format()),
            self.get_view_name(),
            self.request.method,
            self.request.user.username,
            post_data,
            self.request.path,
            get_data,
        )

        # Put sentry capture exception here

        try:
            return super().handle_exception(exc)
        except APINotFound as e:
            return response.Response({"error": e.message, "code": e.code}, status=404)
        except APIForbidden as e:
            return response.Response({"error": e.message, "code": e.code}, status=403)
        except APIConflict as e:
            return response.Response({"error": e.message, "code": e.code}, status=409)
        except (APIException, APIAccessDenied) as e:
            return response.Response({"error": e.message, "code": e.code}, status=400)
        except Exception:
            # Put sentry capture exception here
            return response.Response(
                {"error": "Something went wrong.", "code": "unknown"}, status=500
            )

    def get_instance(self, model, pk, filter=None, **query):
        try:
            if filter:
                return model.objects.filter(filter).get(uid=pk, **query)
            return model.objects.get(uid=pk, **query)
        except model.DoesNotExist:
            raise APINotFound()
