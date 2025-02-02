from collections import defaultdict
from typing import Optional

import pandas as pd
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from etiketle.core.mixins import OnlyAdminsMixin
from etiketle.datasets.forms import DatasetForm
from etiketle.datasets.models import Dataset
from etiketle.datasets.serializers import RedditPostAnnotationSerializer
from etiketle.posts.models import Confidence, RedditPost, RedditPostAnnotation
from etiketle.projects.models import Project


class DatasetListView(LoginRequiredMixin, OnlyAdminsMixin, ListView):
    model = Dataset
    template_name = "datasets/dataset_list.html"


class DatasetDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Dataset
    template_name = "datasets/dataset_detail.html"

    def test_func(self) -> Optional[bool]:
        return True


class DatasetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Dataset
    form_class = DatasetForm
    template_name = "datasets/dataset_form.html"

    def test_func(self) -> Optional[bool]:
        return True


class DatasetCreateView(LoginRequiredMixin, CreateView):
    model = Dataset
    form_class = DatasetForm
    template_name = "datasets/dataset_form.html"

    def form_valid(self, form: DatasetForm) -> HttpResponse:
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        dataset_object = self.object  # type: Dataset
        dataset_object.import_file()
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"].fields["project"].queryset = Project.objects.filter(members__id=self.request.user.id)
        return context


class DatasetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Dataset
    template_name = "datasets/dataset_confirm_delete.html"

    def test_func(self) -> Optional[bool]:
        return True

    def get_success_url(self) -> str:
        dataset = self.get_object()  # type: Dataset
        return reverse("projects:detail", kwargs=dict(pk=dataset.project_id))


class RedditPostListView(LoginRequiredMixin, View):
    template_name = "posts/reddit/post_list.html"

    def get(self, request, *args, **kwargs):
        dataset_pk = kwargs["pk"]
        dataset = Dataset.objects.get(pk=dataset_pk)
        posts = RedditPost.objects.filter(dataset_id=dataset_pk).order_by("id")
        my_annotations = RedditPostAnnotation.objects.filter(user=request.user).values_list("post_id", flat=True)
        data = dict(object_list=posts, dataset=dataset, my_annotations=my_annotations)
        return render(request, self.template_name, data)


class RedditPostListTeamView(LoginRequiredMixin, View):
    template_name = "posts/reddit/post_list_team.html"

    def get(self, request, *args, **kwargs):
        dataset_pk = kwargs["pk"]
        dataset = Dataset.objects.get(pk=dataset_pk)
        posts = RedditPost.objects.filter(dataset_id=dataset.pk)
        team_members = dataset.project.members.all()

        team_annotations = dict(
            [
                (
                    team_member.pk,
                    [an.post_id for an in RedditPostAnnotation.objects.filter(user=team_member, post__in=posts)],
                )
                for team_member in team_members
            ]
        )
        # {1: [4889, 4873, 4875, 4867, 4868, 4869]}
        annotations_dict = defaultdict(list)

        for user_id, post_ids in team_annotations.items():
            for post_id in post_ids:
                annotations_dict[post_id] += [user_id]

        data = dict(object_list=posts, dataset=dataset, annotations_dict=annotations_dict)
        return render(request, self.template_name, data)


def _get_dataset_as_df(pk):
    dataset = Dataset.objects.get(pk=pk)
    data = [post.data for post in dataset.posts.all()]
    df = pd.DataFrame.from_records(data)
    df = df[[x for x in df.columns if len(x) >= 1]].set_index("id")

    cols = list(df.columns.values)
    first_cols = [
        "created_utc",
        "subreddit",
        "author",
        "url",
        "title",
        "selftext",
        "num_comments",
        "score",
        "ups",
        "downs",
        "domain",
    ]
    for col in first_cols:
        cols.remove(col)
    for i, col in enumerate(first_cols):
        cols.insert(i, col)
    df = df[cols]
    return df


def export_posts(request, pk):
    df = _get_dataset_as_df(pk)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="dataset{pk}.csv"'
    df.to_csv(path_or_buf=response)  # with other applicable parameters
    return response


def export_annotations(request, pk):
    """
    Exports annotations for a dataset as json
    :param request:
    :param pk:
    :return: json response containing annotations and config
    """
    dataset = Dataset.objects.get(pk=pk)
    annotations = RedditPostAnnotation.objects.filter(post__in=dataset.posts.all())
    annotation_dict = defaultdict(list)
    for annotation in annotations:
        reddit_id = annotation.post.data["id"]  # type: str
        annotation_dict[reddit_id] += [RedditPostAnnotationSerializer(annotation).data]

    options_dict = dict([(option.pk, option.text) for option in dataset.annotation_config.options.all()])
    confidence_dict = dict(Confidence.choices)
    result = {
        "dataset_id": dataset.pk,
        "options": options_dict,
        "confidence": confidence_dict,
        "annotations": annotation_dict,
    }
    if request.GET.get("inline"):
        return JsonResponse(result)

    response = JsonResponse(result, content_type="text/json")
    response["Content-Disposition"] = f'attachment; filename="dataset{pk}-annotations.json"'
    return response


def dataset_annotation_statistics(request, pk: int):
    """Displays statistics about the dataset annotation"""
    dataset = Dataset.objects.get(pk=pk)
    annotation_counts = dict(
        [
            (
                member,
                RedditPostAnnotation.objects.filter(post__dataset_id=dataset.pk).filter(user_id=member.pk).count(),
            )
            for member in dataset.project.members.all()
        ]
    )

    data = dict(
        dataset=dataset,
        annotation_counts=annotation_counts,
    )

    return render(request, "datasets/dataset_statistics.html", context=data)
