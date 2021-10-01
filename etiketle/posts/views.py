from typing import Optional

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DeleteView, DetailView, ListView, UpdateView
from werkzeug.exceptions import BadRequest

from etiketle.core.mixins import OnlyAdminsMixin
from etiketle.datasets.models import Dataset
from etiketle.posts.forms import RedditPostAnnotationForm, RedditPostForm
from etiketle.posts.models import RedditPost, RedditPostAnnotation


class RedditPostListView(LoginRequiredMixin, ListView):
    model = RedditPost
    template_name = "posts/reddit/post_list.html"


class RedditPostDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = RedditPost
    template_name = "posts/reddit/post_detail.html"

    def test_func(self) -> Optional[bool]:
        return True


def get_dataset_options(pk: int):
    key = f"dataset:{pk}:options"
    options = cache.get(key)
    if options:
        print("cached", options)
        return options
    else:
        dataset = get_object_or_404(Dataset, pk=pk)
        options = dataset.annotation_config.options.all()
        cache.set(key, options, 60 * 60)  # store for 1 hour
        print(options)
        return options


def reddit_post_detail_view(request, pk):
    template_name = "posts/reddit/post_detail.html"
    post = get_object_or_404(RedditPost, pk=pk)
    annotation_config = post.dataset.annotation_config
    if request.method == "GET":
        try:
            annotation = RedditPostAnnotation.objects.get(post_id=post.pk)
            form = RedditPostAnnotationForm(
                annotation_config=annotation_config, instance=annotation
            )
        except RedditPostAnnotation.DoesNotExist:
            form = RedditPostAnnotationForm(annotation_config=annotation_config)

        data = dict(object=post, form=form)
        return render(request, template_name, data)
    elif request.method == "POST":
        try:
            annotation = RedditPostAnnotation.objects.get(user=request.user, post=post)
            form = RedditPostAnnotationForm(
                annotation_config, request.POST, instance=annotation
            )
        except RedditPostAnnotation.DoesNotExist:
            form = RedditPostAnnotationForm(annotation_config, request.POST)

        if form.is_valid():
            annotation = form.save(commit=False)
            annotation.post = post
            annotation.user = request.user
            annotation.save()
            annotation.options.set(form.cleaned_data["options"])
            return HttpResponseRedirect(post.next())
        else:
            data = dict(object=post, form=form)
            return render(request, template_name, data)
    else:
        raise BadRequest("Invalid request type. Valid options: GET, PUT")


class RedditPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RedditPost
    form_class = RedditPostForm
    template = "posts/reddit/post_form.html"

    def test_func(self) -> Optional[bool]:
        return True


class RedditPostDeleteView(LoginRequiredMixin, OnlyAdminsMixin, DeleteView):
    model = RedditPost
    template_name = "posts/reddit/post_confirm_delete.html"

    def test_func(self) -> Optional[bool]:
        return True

    def get_success_url(self) -> str:
        post = self.get_object()
        return reverse("datasets:list-posts", kwargs=dict(pk=post.dataset_id))
