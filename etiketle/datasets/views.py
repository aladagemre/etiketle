from typing import Optional

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from etiketle.core.mixins import OnlyAdminsMixin
from etiketle.datasets.forms import DatasetForm
from etiketle.datasets.models import Dataset
from etiketle.posts.models import RedditPost, RedditPostAnnotation
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
        context["form"].fields["project"].queryset = Project.objects.filter(
            members__id=self.request.user.id
        )
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
        posts = RedditPost.objects.filter(dataset_id=dataset_pk)
        my_annotations = RedditPostAnnotation.objects.filter(
            user=request.user
        ).values_list("post_id", flat=True)
        data = dict(object_list=posts, dataset=dataset, my_annotations=my_annotations)
        return render(request, self.template_name, data)
