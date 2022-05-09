import random
from hashlib import sha1
from typing import Callable, Dict, List, Optional, Type

import pandas as pd
import tensorflow_datasets as tfds
from annotationsdatabase import models
from django.core.management.base import BaseCommand
from tqdm import tqdm


class Command(BaseCommand):
    help = "Load annotations into the SQL annotations database from a CSV file"

    BULK_CREATE_BATCH_SIZE = 1000

    def handle(self, *args, **kwargs):
        annotations = self.load_annotations()

        self.upsert_model_instances(
            model_class=models.ImageAnnotation,
            instances=annotations.to_dict(orient="records"),
            logger=self.stdout.write,
        )

    @staticmethod
    def upsert_model_instances(
        model_class: Type[models.ModelType],
        instances: List[Dict],
        logger: Optional[Callable[[str], None]] = None,
    ):
        logger = logger or (lambda _: ...)
        logger(f"Loading {model_class.__name__} ...")

        n_created = 0

        for instance_dict in tqdm(instances):
            instance, created = model_class.objects.update_or_create(**instance_dict)
            n_created += created

        logger(
            f"Successfully loaded {len(instances)} {model_class.__name__} "
            f"(created={n_created}, existed={len(instances) - n_created})"
        )

    @staticmethod
    def load_annotations() -> pd.DataFrame:
        (ok_ds, ko_ds, to_review) = tfds.load(
            "tf_flowers", split=["train[:80%]", "train[80%:82%]", "train[82%:]"]
        )
        label_mapping = {
            0: "dandelion",
            1: "daisy",
            2: "tulips",
            3: "sunflowers",
            4: "roses",
        }

        return pd.concat(
            [
                tfds.as_dataframe(ds)
                .assign(
                    image_id=lambda df: df.image.map(lambda x: sha1(x).hexdigest()),
                    label=lambda df: df.label.map(label_mapping),
                    height=lambda df: df.image.map(lambda x: x.shape[0]),
                    width=lambda df: df.image.map(lambda x: x.shape[1]),
                    label_correctness=["OK", "TO_BE_CHECKED"][index],
                    image_correctness="OK",
                )
                .drop(columns=["image"])
                for index, ds in enumerate([ok_ds, to_review])
            ]
            + [
                tfds.as_dataframe(ko_ds)
                .assign(
                    image_id=lambda df: df.image.map(lambda x: sha1(x).hexdigest()),
                    label=lambda df: df.label.map(
                        lambda _: random.choice(list(label_mapping.values()))
                    ),
                    height=lambda df: df.image.map(lambda x: x.shape[0]),
                    width=lambda df: df.image.map(lambda x: x.shape[1]),
                    label_correctness="KO",
                    image_correctness="OK",
                )
                .drop(columns=["image"])
            ]
        )
