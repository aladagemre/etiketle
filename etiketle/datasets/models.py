from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from etiketle.datasets.importers import RedditPostImporter
from etiketle.projects.models import Project


class Dataset(TimeStampedModel):
    class Source(models.TextChoices):
        REDDIT_POST = "RDTP", _("Reddit Post")

    name = models.CharField(max_length=50)
    file = models.FileField()
    source = models.CharField(
        choices=Source.choices, max_length=50, default=Source.REDDIT_POST
    )
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

    def import_file(self):
        if self.source == self.Source.REDDIT_POST:
            importer = RedditPostImporter(self)
            importer.start()
