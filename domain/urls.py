from django.urls import path, include
from django.views.generic import TemplateView

from domain.views import InviteFormView, RemoveSalesman

app_name = 'domain'

urlpatterns = [
    # Views
    path('salesman/<str:name>', TemplateView.as_view(template_name='dashboard/salesman.html'), name='salesman'),
    path('', TemplateView.as_view(template_name='dashboard/domain.html'), name='detail'),

    # Actions
    path('invite', InviteFormView.as_view(), name='invite'),
    path('salesman/<int:id>/remove', RemoveSalesman.as_view(), name='remove')
    
]
