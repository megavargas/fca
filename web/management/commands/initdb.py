import os
import time
import random
import datetime

from faker import Faker
fake = Faker()

from domain.models import Domain
from client.models import Client, Manager
from agent.models import Agent
from opportunity.models import Competitor, CompetitorOpportunity, Opportunity, Requirement, Requirement, ManagerOpportunity

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = ''
    help = 'Populate Database'

    def __init__(self):
        super(Command, self).__init__()

    def add_arguments(self, parser):

        parser.add_argument(
            '--action',
            default=False,
            action='store_true',
            dest='action',            
            help='Create production data',
        )

    def handle(self, *args, **options):

        # Create domain
        domain = Domain(name='pass.com')
        domain.save()
        
        # Create owner
        agent = Agent.objects.create_user(email='vargas@pass.com', password='pass')
        agent.is_owner = True
        agent.domain = domain
        agent.save()

        # Create salesteam
        for i in range(random.randrange(12)):
            agent = Agent.objects.create_user(email='salesman' + str(i) + '@pass.com', password='pass')
            agent.domain = domain
            agent.save()
        
        # Create clients
        for _ in range(random.randrange(1,24)):
            client = Client(name=fake.company())
            client.save()

            # Create managers
            for _ in range(random.randrange(12)):
                Manager(client = client, first_name = fake.first_name(), last_name = fake.last_name(), title = fake.job(), email = fake.free_email(), phone = fake.phone_number()).save()

        # Create competitors
        for _ in range(random.randrange(24)):
            competitor = Competitor(name=fake.company())
            competitor.save()

        # Create opportunities
        for _ in range(random.randrange(60)):

            cmp_count = random.randint(2,12)
            opportunity = Opportunity(          
                agent = random.choice(Agent.objects.all()), \
                client = random.choice(Client.objects.all()), \
                created = datetime.datetime.now() - datetime.timedelta(days=random.randrange(12)), \
                updated = datetime.datetime.now(), \
                deadline = datetime.datetime.now() + datetime.timedelta(days=random.randrange(12)), \
                budget = 60000 + (random.randrange(60)*1000), \
                margin = random.randrange(40)/100, \
                # Relationship
                rel_knowledge = random.choice([True,False]), \
                # Competitors
                cmp_knowledge = random.choice([True,False]), \
                cmp_count = cmp_count, \
                # Solution
                sol_leader = random.choice([True,False]), \
                sol_refs = random.choice([True,False]), \
                sol_understanding = random.choice([True,False]), \
                sol_quantify = random.choice([True,False]), \
                sol_create_requirements = random.choice([True,False]), \
                sol_negociation = random.choice([True,False]))

            opportunity.save()

            for _ in range(random.randrange(cmp_count)):

                CompetitorOpportunity(
                    competitor = random.choice(Competitor.objects.all()), \
                    opportunity = opportunity, \
                    appreciation = random.choice(CompetitorOpportunity.APPRECIATION)[0], \
                    relationship = random.choice(CompetitorOpportunity.RELATIONSHIP)[0], \
                    fullfilment = random.choice(CompetitorOpportunity.FULLFILMENT)[0], \
                    pro = fake.sentence(nb_words=26), \
                    cons = fake.sentence(nb_words=26), \
                    notes = fake.sentence(nb_words=26)
                ).save()

            for _ in range(random.randrange(6)):

                Requirement(
                    description = fake.sentence(nb_words=6), \
                    opportunity = opportunity, \
                    fulfillment = random.choice(Requirement.FULLFILMENT)[0], \
                    notes = fake.sentence(nb_words=16)                  
                ).save()






        
        
