from django.db import models

from core.models import BaseModel


class Todo(BaseModel):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    done = models.BooleanField(default=False)

    def __str__(self) -> str:
        done = "Done" if self.done else "Not finished"
        return f"Todo: {self.name} | {done}"
