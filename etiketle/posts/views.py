from typing import Optional

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import DeleteView, DetailView, ListView, UpdateView

from etiketle.core.mixins import OnlyAdminsMixin
from etiketle.posts.forms import RedditPostForm
from etiketle.posts.models import RedditPost


class RedditPostListView(LoginRequiredMixin, ListView):
    model = RedditPost
    template_name = "posts/reddit/post_list.html"


class RedditPostDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = RedditPost
    template_name = "posts/reddit/post_detail.html"

    def test_func(self) -> Optional[bool]:
        return True


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
