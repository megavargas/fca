from django.db import models

from agent.models import Agent
from client.models import Client, Manager
from domain.models import Domain

from django.dispatch import receiver
from django.db.models.signals import post_save

import datetime

class Opportunity(models.Model):

    MILESTONE_0 = 0
    MILESTONE_1 = 1
    MILESTONE_2 = 2
    MILESTONE_3 = 3
    MILESTONE_4 = 4
    MILESTONE_5 = 5
    MILESTONE_6 = 6
    MILESTONE_7 = 7
    MILESTONE_8 = 8

    MILESTONES = (
        (MILESTONE_0,'Posible Lead'),
        (MILESTONE_1,'Homologación: Homologarse como proveedor. Este hito debe ser cubierto previo al hito 5 en cualquier momento. Evidencia : Correo electrónico.'),
        (MILESTONE_2,'Necesidad admitida: El cliente admite el problema. Evidencia: correo electrónico.'),
        (MILESTONE_3,'Posible solucionador de la necesidad reconocido por el cliente. Evidencia: Correo eletrónico'),
        (MILESTONE_4,'Existencia de proyecto: Fecha  y presupuesto para satisfacer esa necesidad en la empresa.Evidencia:e-mail'),
        (MILESTONE_5,'Invitado a la RFP. Dentro de la Short list de la invitacion a la RFP. Evidencia:e-mail'),
        (MILESTONE_6,'Recepción de la RFP. Evidencia : e-mail'),
        (MILESTONE_7,'Respuesta a la RFP. Entrega de la oferta con la solución propuesta. Evidencia: e-mail'),
        (MILESTONE_8,'Adjudicacion .Comunicación de la adjudicación ganada, perdida o  desierta.Evidencia: e-mail'),
    )

    WIN = 0
    LOST = 1
    CANCELED = 2
    ACTIVE = 3

    STATUS = (
        (WIN, 'Ganada'),
        (LOST, 'Perdida'),
        (CANCELED, 'Cancelada'),
        (ACTIVE, 'Activa'),
    )


    title = models.TextField()

    # Relationships
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='opportunities')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='opporunities')
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='opporunities')

    # Timings
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deadline = models.DateField()

    # Economics
    budget = models.PositiveIntegerField(default=0)
    margin = models.FloatField(default=0)

    # Status
    status = models.PositiveIntegerField(choices=STATUS, default=4)

    # Milestone
    milestone = models.IntegerField(choices=MILESTONES, default=0)

    # Relationship
    rel_knowledge = models.BooleanField(default=False)

    # Competitors
    cmp_knowledge = models.BooleanField(default=False)
    cmp_count = models.PositiveIntegerField(default=0)

    # Solution
    sol_leader = models.BooleanField(default=False)
    sol_refs = models.BooleanField(default=False)
    sol_understanding = models.BooleanField(default=False)
    sol_quantify = models.BooleanField(default=False)
    sol_create_requirements = models.BooleanField(default=False)
    sol_negociation = models.BooleanField(default=False)
    

class Activity(models.Model):
    agent = models.ForeignKey(Agent, on_delete = models.CASCADE, related_name='activities')
    domain = models.ForeignKey(Domain, on_delete = models.CASCADE, related_name='activities')
    opportunity = models.ForeignKey(Opportunity, on_delete = models.CASCADE, related_name='activities')
    client = models.ForeignKey(Client, on_delete = models.CASCADE, related_name='activities')
    icon = models.CharField(max_length=16)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()


class OpportunityHistory(models.Model):

    opportunity = models.ForeignKey(Opportunity, on_delete = models.CASCADE, related_name='history')
    date = models.DateField(auto_now_add=True)
    value = models.PositiveIntegerField(default=0)
    milestone = models.PositiveIntegerField(default=0)

class ManagerOpportunity(models.Model):

    USER = 0
    TECHNICAL_DECISOR = 1
    TECHNICAL_PROSPECTOR = 2
    ECONMICAL_DECISOR = 1
    ECONMICAL_PROSPECTOR = 2
    
    ROLE = (
        (TECHNICAL_DECISOR,'Decisor técnico'),
        (TECHNICAL_PROSPECTOR,'Prospector técnico'),
        (ECONMICAL_DECISOR,'Decisor económico'),
        (ECONMICAL_PROSPECTOR,'Prospector económico'),
    )
    
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, blank=True, null=True, related_name='manages')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='managers')
    actitude = models.BooleanField()

    note = models.TextField()

class Competitor(models.Model):
    name = models.CharField(max_length=160) 

class CompetitorOpportunity(models.Model):

    BAD = -1
    NEUTRAL = 0
    GOOD = 1

    APPRECIATION = (
        (BAD, 'En contra'),
        (NEUTRAL, 'Neutral'),
        (GOOD, 'A Favor'),
    )


    NO_RELATIONSHIP = 0
    RELATIONSHIP_POSITIVE = 1
    RELATIONSHIP_NEGATIVE = 1

    RELATIONSHIP = (
        (NO_RELATIONSHIP, 'No existe relación'),
        (RELATIONSHIP_POSITIVE, 'Hay una relación previa positiva'),
        (RELATIONSHIP_NEGATIVE, 'Hay una relación previa negativa'),
    )

    NONE = 0
    BASIC = 1
    COMPLETE = 2
    OUTPERFORMS = 3

    FULLFILMENT = (
        (NONE,'Ninguna'),
        (BASIC,'Básica'),
        (COMPLETE,'Completa'),
        (OUTPERFORMS,'Excede'),
    )

    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='competitors')
    appreciation = models.IntegerField(default=0, choices=APPRECIATION)
    relationship = models.IntegerField(default=0, choices=RELATIONSHIP)
    fullfilment = models.PositiveIntegerField(default=0, choices=FULLFILMENT)

    pro = models.TextField()
    cons = models.TextField()
    notes = models.TextField()

class Requirement(models.Model):

    NONE = 0
    BASIC = 1
    COMPLETE = 2
    OUTPERFORMS = 3

    FULLFILMENT = (
        (NONE,'Ninguna'),
        (BASIC,'Básica'),
        (COMPLETE,'Completa'),
        (OUTPERFORMS,'Excede'),
    )

    description = models.TextField()
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='requirements')
    fulfillment = models.PositiveIntegerField(default=0, choices=FULLFILMENT)
    notes = models.TextField()


@receiver(post_save, sender=Requirement)
def register_requirement_update(sender, instance, **kwargs):

    # Create activity update
    agent = instance.opportunity.agent
    domain = instance.opportunity.domain
    opportunity = instance.opportunity
    client = instance.opportunity.client
    icon = 'user'
    description = 'Requisito actualizado'
    Activity(agent=agent, domain=domain, opportunity=opportunity, client=client, icon=icon, description=description).save()

@receiver(post_save, sender=CompetitorOpportunity)
def register_competitor_update(sender, instance, **kwargs):

    # Create activity update
    agent = instance.opportunity.agent
    domain = instance.opportunity.domain
    opportunity = instance.opportunity
    client = instance.opportunity.client
    icon = 'user'
    description = 'Competidor actualizado: ' + instance.competitor.name
    Activity(agent=agent, domain=domain, opportunity=opportunity, client=client, icon=icon, description=description).save()

# Signals
@receiver(post_save, sender=ManagerOpportunity)
def register_manager_update(sender, instance, **kwargs):

    # Create activity update
    agent = instance.opportunity.agent
    domain = instance.opportunity.domain
    opportunity = instance.opportunity
    client = instance.opportunity.client
    icon = 'user'
    description = 'Decisor actualizado: ' + instance.manager.email
    Activity(agent=agent, domain=domain, opportunity=opportunity, client=client, icon=icon, description=description).save()

# Signals
@receiver(post_save, sender=Opportunity)
def register_opportunity_history(sender, instance, **kwargs):

    # Value calculation
    status = 1 if instance.status in [0,3] else 0
    value = (instance.milestone * (100/8)) * status
    budget = instance.budget * value
    defaults = {'value': value, 'milestone': instance.milestone}

    # History record
    OpportunityHistory.objects.update_or_create(date=datetime.date.today(), opportunity=instance, defaults=defaults)

    # Create activity update
    agent = instance.agent
    domain = instance.domain
    opportunity = instance
    client = instance.client
    icon = 'user'
    description = 'Oportunidad actualizada'
    Activity(agent=agent, domain=domain, opportunity=opportunity, client=client, icon=icon, description=description).save()