# -*- coding: utf-8 -*-
from django.urls import path

from . import views

app_name = "teams"

urlpatterns = [
    path(
        route="",
        view=views.TeamListView.as_view(),
        name="list",
    ),
    path(
        route="add/",
        view=views.TeamCreateView.as_view(),
        name="add",
    ),
    path(
        route="<int:pk>/",
        view=views.TeamDetailView.as_view(),
        name="detail",
    ),
    path(
        route="<int:pk>/update/",
        view=views.TeamUpdateView.as_view(),
        name="update",
    ),
]
