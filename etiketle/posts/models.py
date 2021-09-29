from django.conf import settings
from django.db import models
from django.urls import reverse
from model_utils.models import TimeStampedModel


class RedditPost(models.Model):
    #   warnings.warn("DateTimeField %s received a naive datetime (%s)"
    dataset = models.ForeignKey(
        "datasets.Dataset",
        on_delete=models.CASCADE,
        related_name="posts",
        db_index=True,
    )

    created_at = models.DateTimeField(blank=True, null=True)
    subreddit = models.CharField(max_length=50, db_index=True)
    url = models.URLField()
    data = models.JSONField()

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs=dict(pk=self.id))

    def __str__(self):
        title = self.data.get("title")
        return f"[{self.subreddit}] {title}"


class Confidence(models.IntegerChoices):
    NOT_CONFIDENT = 0, "Not confident at all"
    SOMEHOW_CONFIDENT = 1, "Somehow confident"
    VERY_CONFIDENT = 4, "Very confident"
    ABSOLUTELY_SURE = 5, "Absolutely sure"


class RedditPostAnnotation(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reddit_annotations",
        db_index=True,
    )
    post = models.ForeignKey(
        RedditPost,
        on_delete=models.CASCADE,
        related_name="annotations",
    )
    options = models.ManyToManyField(
        "datasets.AnnotationOption",
        related_name="annotations",
    )
    notes = models.TextField()
    confidence = models.IntegerField(choices=Confidence.choices)
