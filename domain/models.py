from django.db import models

# Create your models here.
class Domain(models.Model):

    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to = 'logos/', default = 'logos/no-logo.png')
