from django.conf import settings
from django.db import models
from django.urls import reverse
from model_utils.models import TimeStampedModel

from etiketle.teams.models import Team


class Project(TimeStampedModel):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="created_by",
        null=True,
    )
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name="projects")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="projects")

    def __str__(self):
        return f"Team {self.team.name}'s Project: {self.name}"

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs=dict(pk=self.id))


class AnnotationConfig(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="annotation_configs",
    )

    def __str__(self):
        return self.name


class AnnotationOption(models.Model):
    config = models.ForeignKey(
        AnnotationConfig,
        on_delete=models.CASCADE,
        related_name="options",
    )
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text
