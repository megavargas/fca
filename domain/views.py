from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.mail import send_mail

from django.views.generic.edit import FormView
from fuser.models import FUser

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from braces.views import UserPassesTestMixin, LoginRequiredMixin

from .forms import InviteActionForm, DeleteActionForm


class SalesManView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):

    template_name = 'dashboard/salesman.html'

    def test_func(self, user):
        salesman_name = self.request.get_full_path().split('/')[-1]
        salesman_email = salesman_name + '@' + user.domain.name
        self.salesman = get_object_or_404(FUser, email=salesman_email)

        return (user.is_owner or user==self.salesman) and self.salesman

    

class InviteFormView(FormView):
    template_name = 'dashboard/invite.html'
    form_class = InviteActionForm
    success_url = reverse_lazy('domain:detail')

    def form_valid(self, form):
        for email in form.cleaned_data['emails'].split(','):
            send_mail(
                'Subject here',
                'Here is the message.',
                'info@forecash.net',
                [email],
                fail_silently=False,
            )
        messages.add_message(request.request, messages.INFO, 'Hello world.')
        return super().form_valid(form)


class RemoveSalesman(FormView):
    template_name = 'dashboard/remove_salesman.html'
    form_class = DeleteActionForm
    success_url = reverse_lazy('domain:detail')

    def form_valid(self, form):
        FUser.objects.get(id=form.cleaned_data['id']).delete()
        messages.add_message(request.request, messages.INFO, 'Hello world.')
        return super().form_valid(form)

