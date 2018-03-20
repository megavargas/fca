from django.urls import path, include
from django.views.generic import TemplateView

from domain.views import InviteFormView, RemoveSalesman, SalesManView

app_name = 'domain'

urlpatterns = [
    # Views
    path('salesman/<str:name>', SalesManView.as_view(template_name='dashboard/salesman.html'), name='salesman'),
    path('domain/', TemplateView.as_view(template_name='dashboard/domain.html'), name='detail'),

    # Actions
    path('domain/invite/', InviteFormView.as_view(), name='invite'),
    path('salesman/<str:name>/remove', RemoveSalesman.as_view(), name='remove')
    
]
