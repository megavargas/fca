from django.urls import path, include
from django.views.generic import TemplateView

from domain.views import InviteFormView, RemoveSalesman, SalesManView

app_name = 'salesman'

urlpatterns = [
    # Views
    # path('salesman/<str:name>/remove', RemoveSalesman.as_view(), name='remove')
    # path('salesman/<str:name>', SalesManView.as_view(template_name='dashboard/salesman.html'), name='salesman'),
    
]
