import uuid

from django.db import models


class AbstractBaseModel(models.Model):
    """
    This abstract class contains the common fields for all models.
    See https://docs.djangoproject.com/fr/4.0/topics/db/models/#abstract-base-classes
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class QualityTagValues(models.TextChoices):
    """
    This class contains the default possible values for the quality tag.
    """

    KO = "KO"
    TO_BE_CHECKED = "TO_BE_CHECKED"
    OK = "OK"


def get_quality_tag_field() -> models.CharField:
    return models.CharField(max_length=24, choices=QualityTagValues.choices, default=QualityTagValues.TO_BE_CHECKED)
