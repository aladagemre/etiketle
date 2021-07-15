from typing import Optional

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from etiketle.core.mixins import OnlyAdminsMixin
from etiketle.projects.forms import ProjectForm
from etiketle.projects.models import Project
from etiketle.teams.models import Team


class ProjectListView(LoginRequiredMixin, OnlyAdminsMixin, ListView):
    model = Project
    template_name = "projects/project_list.html"


class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Project
    template_name = "projects/project_detail.html"

    def test_func(self) -> Optional[bool]:
        return True


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"

    def form_valid(self, form: ProjectForm) -> HttpResponse:
        form.instance.created_by = self.request.user
        self.object = form.save(commit=False)
        self.object.save()
        self.object.members.set([self.request.user])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"].fields["team"].queryset = Team.objects.filter(
            members__id=self.request.user.id
        )
        return context


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"

    def test_func(self) -> Optional[bool]:
        return True


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_confirm_delete.html"

    def test_func(self) -> Optional[bool]:
        return True
