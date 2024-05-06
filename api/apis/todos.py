from http import HTTPStatus

from rest_framework.response import Response

from api.base import BaseAPI
from api.serializers.todos import TodoSerializer
from todos.models import Todo


class TodoAPI(BaseAPI):
    def list(self, request):
        serializer = TodoSerializer(Todo.objects.filter(user=request.user), many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk):
        instance = self.get_instance(
            model=Todo,
            pk=pk,
        )
        return Response(TodoSerializer(instance=instance).data)

    def create(self, request):
        data = TodoSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data.save(user=request.user)

        return Response(data.data)

    def update(self, request, *args, **kwargs):
        data = TodoSerializer(
            instance=self.get_instance(
                model=Todo,
                pk=kwargs.get("pk"),
            ),
            data=request.data,
            partial=True,
        )
        data.is_valid(raise_exception=True)
        data.save()

        return Response(TodoSerializer(instance=data.instance).data)

    def delete(self, request, pk):
        instance = self.get_instance(
            model=Todo,
            pk=pk,
        )
        instance.delete()

        return Response(status=HTTPStatus.NO_CONTENT)
