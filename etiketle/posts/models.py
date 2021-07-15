from django.db import models


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

    def __str__(self):
        title = self.data.get("title")
        return f"[{self.subreddit}] {title}"
