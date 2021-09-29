# -*- coding: utf-8 -*-
from django.urls import path

from . import views

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
