# -*- coding: utf-8 -*-
from django import forms

from etiketle.projects.models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ["created_by", "members"]
