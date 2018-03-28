from django.views.generic import UpdateView, DeleteView, ListView, DetailView

from django.shortcuts import get_object_or_404
from braces.views import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Agent, AgentProfile
from opportunity.models import Opportunity, OpportunityHistory
import datetime

class AgentRemoveActionView(DeleteView):
    pass


class AgentUpdateActionView(UserPassesTestMixin, SuccessMessageMixin, UpdateView):

    model = AgentProfile
    fields = ['phone','first_name','last_name','title']
    success_message = "Actualizado"

    def test_func(self, user):
        email = self.request.path.split('/')[2]
        self.agent = get_object_or_404(Agent, email=email)
        return (self.agent == user)

    def get_object(self):
        return self.agent.profile

class AgentDetailView(LoginRequiredMixin, DetailView):

    template_name = 'agent/detail.html'

    def get_object(self):
        email = self.request.GET['email'] if ('email' in self.request.GET.keys() and self.request.user.is_owner) else self.request.user.email
        return get_object_or_404(Agent, email=email)