from django.db import models

# Create your models here.
from agent.models import Agent
from domain.models import Domain
from client.models import Client
from opportunity.models import Opportunity

class Activity(models.Model):
    agent = models.ForeignKey(Agent, on_delete = models.CASCADE, related_name='activities')
    domain = models.ForeignKey(Domain, on_delete = models.CASCADE, related_name='activities')
    opportunity = models.ForeignKey(Opportunity, on_delete = models.CASCADE, related_name='activities')
    client = models.ForeignKey(Client, on_delete = models.CASCADE, related_name='activities')
    icon = models.CharField(max_length=16)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
