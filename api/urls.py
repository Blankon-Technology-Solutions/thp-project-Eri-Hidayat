from django.urls import include, path
from rest_framework import routers

from api.apis import accounts, todos

api_router = routers.DefaultRouter()
api_router.register(r"accounts", accounts.AccountAPI, basename="account")
api_router.register(r"todos", todos.TodoAPI, basename="todo")


urlpatterns = [
    path("api/", include(api_router.urls)),
]
