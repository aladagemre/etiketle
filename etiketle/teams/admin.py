from django.contrib import admin

from etiketle.teams.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass
