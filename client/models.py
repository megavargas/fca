from django.db import models

# Create your models here.

class Client(models.Model):

    name = models.CharField(max_length=160)

class Manager(models.Model):

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='managers')
    first_name = models.CharField(max_length=160)
    last_name = models.CharField(max_length=160)
    title = models.CharField(max_length=160)
    email = models.CharField(max_length=160)
    phone = models.CharField(max_length=160)
    address = models.CharField(max_length=160)