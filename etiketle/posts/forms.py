# -*- coding: utf-8 -*-
from django import forms

from etiketle.posts.models import RedditPost


class RedditPostForm(forms.ModelForm):
    class Meta:
        model = RedditPost
        fields = "__all__"
