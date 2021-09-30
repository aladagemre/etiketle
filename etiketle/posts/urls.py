# -*- coding: utf-8 -*-
from django.urls import path

from . import views
from .views import reddit_post_detail_view

app_name = "posts"

urlpatterns = [
    path(
        route="reddit/",
        view=views.RedditPostListView.as_view(),
        name="list",
    ),
    path(
        route="reddit/<int:pk>/",
        view=reddit_post_detail_view,
        name="detail",
    ),
    path(
        route="reddit/<int:pk>/update/",
        view=views.RedditPostUpdateView.as_view(),
        name="update",
    ),
]
