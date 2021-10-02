from django.conf import settings
from django.db import models
from django.urls import reverse
from model_utils.models import TimeStampedModel


class Team(TimeStampedModel):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="founded_teams",
        null=True,
    )
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="teams")

    def get_absolute_url(self):
        return reverse("teams:detail", kwargs=dict(pk=self.id))

    def __str__(self):
        return f"Team {self.name}"
