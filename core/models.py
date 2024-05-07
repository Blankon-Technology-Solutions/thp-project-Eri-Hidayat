from bson import objectid
from django.db import models


def set_objectid():
    return str(objectid.ObjectId())


class BaseModel(models.Model):
    uid = models.CharField(
        default=set_objectid, db_index=True, unique=True, max_length=32
    )
    user = models.ForeignKey(
        "auth.User", null=True, blank=True, on_delete=models.SET_NULL
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-uid"]
