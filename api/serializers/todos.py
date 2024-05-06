from rest_framework import serializers

from todos.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="uid", required=False)

    class Meta:
        model = Todo
        fields = ["id", "name", "description", "done"]
