# -*- coding: utf-8 -*-
from django import forms

from etiketle.datasets.models import Dataset


class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        exclude = ["created_by"]
