from django.conf import settings
from django.db import models
from django.urls import reverse
from model_utils.models import TimeStampedModel

from etiketle.projects.models import Project


class Dataset(TimeStampedModel):
    name = models.CharField(max_length=50)
    file = models.FileField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="uploader"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="datasets"
    )
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return f"Project {self.project.name}'s Dataset: {self.name}"

    def get_absolute_url(self):
        return reverse("datasets:detail", kwargs=dict(pk=self.id))
