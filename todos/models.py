from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from core.models import BaseModel


class Todo(BaseModel):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    done = models.BooleanField(default=False)

    def __str__(self) -> str:
        done = "Done" if self.done else "Not finished"
        return f"Todo: {self.name} | {done}"


@receiver(post_save, sender=Todo)
def send_update_message(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        instance.uid,
        {
            "type": f"todo_{'created' if created else 'updated'}",
            "message": {
                "id": instance.uid,
                "name": instance.name,
                "description": instance.description,
                "done": instance.done,
            },
        },
    )


@receiver(post_delete, sender=Todo)
def send_delete_message(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        instance.uid,
        {
            "type": "todo_deleted",
            "message": {
                "id": instance.uid,
            },
        },
    )
