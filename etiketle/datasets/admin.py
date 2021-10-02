from django.contrib import admin

from etiketle.datasets.models import Dataset


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    pass
