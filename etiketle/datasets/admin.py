from django.contrib import admin

from etiketle.datasets.models import AnnotationConfig, AnnotationOption, Dataset


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    pass


@admin.register(AnnotationConfig)
class AnnotationConfigAdmin(admin.ModelAdmin):
    pass


@admin.register(AnnotationOption)
class AnnotationOptionAdmin(admin.ModelAdmin):
    pass
