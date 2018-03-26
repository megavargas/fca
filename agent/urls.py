from django.urls import path, include
from django.views.generic import TemplateView

from .views import AgentRemoveActionView, AgentDetailView

app_name = 'agent'

urlpatterns = [
    # Views
    path('<str:email>/remove', AgentRemoveActionView.as_view(), name='remove'),
    path('<str:email>', AgentDetailView.as_view(), name='detail'),
    path('', AgentDetailView.as_view(), name='detail'),
    
]
