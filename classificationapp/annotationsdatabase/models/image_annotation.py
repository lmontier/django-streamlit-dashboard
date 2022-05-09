from django.contrib import admin
from django.db import models

from .common import AbstractBaseModel, get_quality_tag_field


class ImageAnnotation(AbstractBaseModel):
    image_id = models.CharField(max_length=60, blank=False, null=False)
    label = models.CharField(max_length=60, null=False, blank=False)
    height = models.IntegerField(null=False, blank=False, default=-1)
    width = models.IntegerField(null=False, blank=False, default=-1)
    label_correctness = get_quality_tag_field()
    image_correctness = get_quality_tag_field()

    def __str__(self):
        return str(self.image_id) + "_" + str(self.label)


@admin.register(ImageAnnotation)
class ImageAnnotationAdmin(admin.ModelAdmin):
    list_display = (
        "image_id",
        "label",
        "label_correctness",
        "image_correctness",
        "created_at",
        "updated_at",
    )
