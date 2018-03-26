from django.db import models

from agent.models import Agent
from client.models import Client, Manager

class Opportunity(models.Model):

    MILESTONE_0 = 0
    MILESTONE_1 = 1
    MILESTONE_2 = 2
    MILESTONE_3 = 3
    MILESTONE_4 = 4
    MILESTONE_5 = 5
    MILESTONE_6 = 6
    MILESTONE_7 = 7

    MILESTONES = (
        (MILESTONE_0,'Homologación: Homologarse como proveedor. Este hito debe ser cubierto previo al hito 5 en cualquier momento. Evidencia : Correo electrónico.'),
        (MILESTONE_1,'Necesidad admitida: El cliente admite el problema. Evidencia: correo electrónico.'),
        (MILESTONE_2,'Posible solucionador de la necesidad reconocido por el cliente. Evidencia: Correo eletrónico'),
        (MILESTONE_3,'Existencia de proyecto: Fecha  y presupuesto para satisfacer esa necesidad en la empresa.Evidencia:e-mail'),
        (MILESTONE_4,'Invitado a la RFP. Dentro de la Short list de la invitacion a la RFP. Evidencia:e-mail'),
        (MILESTONE_5,'Recepción de la RFP. Evidencia : e-mail'),
        (MILESTONE_6,'Respuesta  a la RFP. Entrega de la oferta con la solución propuesta. Evidencia: e-mail'),
        (MILESTONE_7,'Adjudicacion .Comunicación de la adjudicación ganada, perdida o  desierta.Evidencia: e-mail'),
    )

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='opportunities')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='opporunities')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deadline = models.DateField()

    budget = models.PositiveIntegerField(default=0)
    margin = models.FloatField(default=0)

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


