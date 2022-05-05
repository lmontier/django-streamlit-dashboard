from typing import Union

from .image_annotation import ImageAnnotation

# When adding a new model, add it 1) to the ALL_MODELS list below, and 2) to the ModelType below.
ALL_MODELS = [ImageAnnotation]

ModelType = Union[ImageAnnotation]
