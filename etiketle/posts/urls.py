# -*- coding: utf-8 -*-
from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path(
        route="",
        view=views.PostListView.as_view(),
        name="list",
    ),
    path(
        route="add/",
        view=views.PostCreateView.as_view(),
        name="add",
    ),
    path(
        route="<int:pk>/",
        view=views.PostDetailView.as_view(),
        name="detail",
    ),
    path(
        route="<int:pk>/update/",
        view=views.PostUpdateView.as_view(),
        name="update",
    ),
]
