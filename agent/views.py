from django.views.generic import UpdateView, DeleteView, ListView, DetailView
from django.views.generic import TemplateView

from django.shortcuts import get_object_or_404
from braces.views import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Agent, AgentProfile
from opportunity.models import Opportunity, OpportunityHistory, Activity

import datetime

import pandas as pd

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

    def last_day_of_month(date):
        if date.month == 12:
            return date.replace(day=31)
        return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)

    def get_object(self):
        email = self.request.GET['email'] if ('email' in self.request.GET.keys() and self.request.user.is_owner) else self.request.user.email
        return get_object_or_404(Agent, email=email)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agent = context['object']

        # Basic filters
        context['clients'] = list(set([opportunity.client for opportunity in Opportunity.objects.filter(agent=agent)]))
        context['status'] = Opportunity.STATUS
        context['milestones'] = Opportunity.MILESTONES

        # Actual filtering
        opportunities = agent.opportunities.all()
        # import ipdb; ipdb.set_trace()

        # Filter by client
        if 'clients' in self.request.GET.keys():
            opportunities = opportunities.filter(client__pk__in=[int(client) for client in self.request.GET.getlist('clients')])

        if 'status' in self.request.GET.keys():
            opportunities = opportunities.filter(status__in=[int(status) for status in self.request.GET.getlist('status')])

        if 'milestones' in self.request.GET.keys():
            opportunities = opportunities.filter(milestone__in=[int(mailestone) for mailestone in self.request.GET.getlist('mailestones')])

        if 'timings' in self.request.GET.keys() and self.request.GET['timings']:

            today = datetime.date.today()

            this_week_start =  today - datetime.timedelta(days=today.weekday())
            this_week_end =  this_week_start + datetime.timedelta(days=6)
            this_month_start =  today - pd.offsets.MonthBegin()
            this_month_end =  today + pd.offsets.BMonthEnd()
            this_quarter_start =  today - pd.offsets.BQuarterBegin()
            this_quarter_end =  today + pd.offsets.BQuarterEnd()
            this_year_start = today - pd.offsets.BYearBegin()
            this_year_end = today + pd.offsets.BYearEnd()

            if '1' == self.request.GET['timings']:
                opportunities = opportunities.filter(deadline__gte=this_week_start).filter(deadline__lte=this_week_end)
            elif '2' == self.request.GET['timings']:
                opportunities = opportunities.filter(deadline__gte=this_month_start).filter(deadline__lte=this_month_end)
            elif '3' == self.request.GET['timings']:
                opportunities = opportunities.filter(deadline__gte=this_quarter_start).filter(deadline__lte=this_quarter_end)
            elif '4' == self.request.GET['timings']:
                opportunities = opportunities.filter(deadline__gte=this_year_start).filter(deadline__lte=this_year_end)
        
        context['opportunities'] = opportunities
        context['activities'] = Activity.objects.filter(agent=agent)[:100]
        context['forecash'] = agent.get_actual_forecash()

        return context