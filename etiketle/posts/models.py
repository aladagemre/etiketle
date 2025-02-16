from django.conf import settings
from django.core.cache import cache
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

    def previous(self):
        first_index_key = f"dataset:{self.dataset_id}:first_index"
        first_index = cache.get(first_index_key)
        if not first_index:
            first_index = RedditPost.objects.filter(dataset_id=self.dataset_id).first().pk
            cache.set(first_index_key, first_index, 60 * 60)
        if self.pk > first_index:
            previous_id = RedditPost.objects.filter(id__lt=self.pk).order_by("id").values_list("id", flat=True).last()
            return reverse("posts:detail", kwargs=dict(pk=previous_id))
        return None

    def next(self):
        last_index_key = f"dataset:{self.dataset_id}:last_index"
        last_index = cache.get(last_index_key)
        if not last_index:
            last_index = RedditPost.objects.filter(dataset_id=self.dataset_id).last().pk
            cache.set(last_index_key, last_index, 60 * 60)
        if self.pk < last_index - 1:
            next_id = RedditPost.objects.filter(id__gt=self.pk).order_by("id").values_list("id", flat=True).first()
            return reverse("posts:detail", kwargs=dict(pk=next_id))
        return None


class Confidence(models.IntegerChoices):
    NOT_CONFIDENT = 0, "Not confident at all"
    SOMEHOW_CONFIDENT = 1, "Somehow confident"
    CONFIDENT = 2, "Confident"
    VERY_CONFIDENT = 3, "Very confident"
    ABSOLUTELY_SURE = 4, "Absolutely sure"


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
        "projects.AnnotationOption",
        related_name="annotations",
    )
    notes = models.TextField(blank=True)
    confidence = models.IntegerField(choices=Confidence.choices, blank=True, null=True)

    class Meta:
        unique_together = [["user", "post"]]

    def __str__(self):
        return f"{self.user.username} on Redit Post {self.post.pk}"
