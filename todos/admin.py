from django.contrib import admin

from todos.models import Todo


# Register your models here.
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ["name", "done", "user"]
