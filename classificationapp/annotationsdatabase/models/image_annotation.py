from django.contrib import admin
from django.db import models

from .common import AbstractBaseModel


class ImageAnnotation(AbstractBaseModel):
    image_id = models.CharField(max_length=60, unique=True)
    label = models.CharField(max_length=60)

    def __str__(self):
        return str(self.image_hash) + "_" + str(self.label)


@admin.register(ImageAnnotation)
class ImageAnnotationAdmin(admin.ModelAdmin):
    list_display = ("image_id", "label", "created_at", "updated_at")
