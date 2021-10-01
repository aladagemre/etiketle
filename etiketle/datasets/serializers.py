# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer

from etiketle.posts.models import RedditPostAnnotation


class RedditPostAnnotationSerializer(ModelSerializer):
    class Meta:
        model = RedditPostAnnotation
        fields = "__all__"
