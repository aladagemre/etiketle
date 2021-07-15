# -*- coding: utf-8 -*-
from django import forms

from etiketle.projects.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ["created_by", "members"]
