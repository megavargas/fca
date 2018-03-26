from django.urls import path, include
from django.views.generic import TemplateView

from domain.views import InviteFormView, RemoveSalesman, SalesManView

app_name = 'domain'

urlpatterns = [
    # Views
    path('domain/', TemplateView.as_view(template_name='dashboard/domain.html'), name='detail'),
    path('domain/invite/', InviteFormView.as_view(), name='invite'),
    
]
