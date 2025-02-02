# -*- coding: utf-8 -*-
from django import forms

from etiketle.posts.models import RedditPost, RedditPostAnnotation
from etiketle.projects.models import AnnotationOption


class RedditPostForm(forms.ModelForm):
    class Meta:
        model = RedditPost
        fields = "__all__"


class RedditPostAnnotationForm(forms.ModelForm):
    options = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = RedditPostAnnotation
        fields = ["options", "notes", "confidence"]

    def __init__(self, annotation_config, *args, **kwargs):
        super(RedditPostAnnotationForm, self).__init__(*args, **kwargs)
        self.fields["options"].queryset = AnnotationOption.objects.filter(config=annotation_config)
