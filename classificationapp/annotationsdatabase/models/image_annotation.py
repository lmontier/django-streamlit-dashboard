from .common import AbstractBaseModel
from django.db import models
from django.contrib import admin


class ImageAnnotation(AbstractBaseModel):
    image_hash = models.CharField(max_length=60, unique=True)
    name = models.CharField(max_length=60, unique=True)

    @property
    def tray_objects_count(self) -> int:
        return self.trayobject_set.count()

    def __str__(self):
        return self.name


@admin.register(ImageAnnotation)
class ContainerLabelAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "tray_objects_count", "created_at", "updated_at")
