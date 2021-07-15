from django.contrib import admin

# from etiketle.datasets.models import Dataset
from etiketle.posts.models import RedditPost


@admin.register(RedditPost)
class RedditPostAdmin(admin.ModelAdmin):
    list_display = ["get_title", "dataset_id", "subreddit"]
    """
    # + ["get_team", "get_project", "get_dataset_name", "subreddit"]

    def get_queryset(self, request):
        return super(RedditPostAdmin, self).get_queryset(request).select_related('dataset')

    def get_team(self, obj):
        return obj.dataset.project.team

    def get_project(self, obj):
        return obj.dataset.project.name

    def get_dataset_name(self, obj):
        return obj.dataset.name

    """

    def get_title(self, obj):
        return obj.data.get("title")
