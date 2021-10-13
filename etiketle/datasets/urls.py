# -*- coding: utf-8 -*-
from django.urls import path

from . import views
from .views import dataset_annotation_statistics

app_name = "datasets"

urlpatterns = [
    # User Profile
    path(
        route="",
        view=views.DatasetListView.as_view(),
        name="list",
    ),
    path(
        route="add/",
        view=views.DatasetCreateView.as_view(),
        name="add",
    ),
    path(
        route="<int:pk>/",
        view=views.DatasetDetailView.as_view(),
        name="detail",
    ),
    path(
        route="<int:pk>/posts/",
        view=views.RedditPostListView.as_view(),
        name="list-posts",
    ),
    path(
        route="<int:pk>/statistics/",
        view=dataset_annotation_statistics,
        name="dataset-statistics",
    ),
    path(
        route="<int:pk>/export/posts",
        view=views.export_posts,
        name="export-posts",
    ),
    path(
        route="<int:pk>/export/annotations",
        view=views.export_annotations,
        name="export-annotations",
    ),
    path(
        route="<int:pk>/posts/team/",
        view=views.RedditPostListTeamView.as_view(),
        name="list-posts-team",
    ),
    path(
        route="<int:pk>/update/",
        view=views.DatasetUpdateView.as_view(),
        name="update",
    ),
    path(
        route="<int:pk>/delete/",
        view=views.DatasetDeleteView.as_view(),
        name="delete",
    ),
]
