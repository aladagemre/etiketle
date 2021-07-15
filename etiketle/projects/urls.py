# -*- coding: utf-8 -*-
from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path(
        route="",
        view=views.ProjectListView.as_view(),
        name="list",
    ),
    path(
        route="add/",
        view=views.ProjectCreateView.as_view(),
        name="add",
    ),
    path(
        route="<int:pk>/",
        view=views.ProjectDetailView.as_view(),
        name="detail",
    ),
    path(
        route="<int:pk>/update/",
        view=views.ProjectUpdateView.as_view(),
        name="update",
    ),
]
