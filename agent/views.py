from django.views.generic import UpdateView, DeleteView, ListView, DetailView

from django.shortcuts import get_object_or_404

from .models import Agent

class AgentRemoveActionView(DeleteView):
    pass

class AgentDetailView(DetailView):

    template_name = 'agent/detail.html'

    def get_object(self):
        email = self.request.GET['email'] if ('email' in self.request.GET.keys() and self.request.user.is_owner) else self.request.user.email
        return get_object_or_404(Agent, email=email)