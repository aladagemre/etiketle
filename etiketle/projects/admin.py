from django.contrib import admin

from etiketle.projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
