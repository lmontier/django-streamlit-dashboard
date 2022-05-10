import os
import sys

import django


def django_setup() -> None:
    """
    Allows to setup Django if it's not already running on a server. Should be called before any Django imports.
    """
    # The DJANGO_SETTINGS_MODULE has to be set to allow us to access django imports
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "classificationapp.settings")

    # This is for setting up django
    django.setup()
