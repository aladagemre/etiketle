from typing import Optional

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from etiketle.core.mixins import OnlyAdminsMixin
from etiketle.teams.forms import TeamForm
from etiketle.teams.models import Team


class TeamListView(LoginRequiredMixin, OnlyAdminsMixin, ListView):
    model = Team
    template_name = "teams/team_list.html"


class TeamDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Team
    template_name = "teams/team_detail.html"

    def test_func(self) -> Optional[bool]:
        return True


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = "teams/team_form.html"

    def form_valid(self, form: TeamForm) -> HttpResponse:
        form.instance.created_by = self.request.user
        self.object = form.save(commit=False)
        self.object.save()
        self.object.members.set([self.request.user])

        return super().form_valid(form)


class TeamUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = "teams/team_form.html"

    def test_func(self) -> Optional[bool]:
        return True


class TeamDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Team
    form_class = TeamForm
    template_name = "teams/team_confirm_delete.html"

    def test_func(self) -> Optional[bool]:
        return True
