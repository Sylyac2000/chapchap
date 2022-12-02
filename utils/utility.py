"""
###### https://code.djangoproject.com/ticket/22999"""
import os
from uuid import uuid4

from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename(object):
    def __init__(self, upload_to):
        self.upload_to = upload_to


    def __call__(self, instance, filename):
        return self.get_path_and_rename(instance, filename)

    def get_path_and_rename(self, instance, filename):

        ext = filename.split('.')[-1] #split par le dot et prendre le dernier element(-1):l'extension
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex[:15], ext)
        # return the whole path to the file
        return os.path.join(self.upload_to, filename)
