from django.contrib import admin

from etiketle.projects.models import AnnotationConfig, AnnotationOption, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(AnnotationConfig)
class AnnotationConfigAdmin(admin.ModelAdmin):
    pass


@admin.register(AnnotationOption)
class AnnotationOptionAdmin(admin.ModelAdmin):
    pass
