from django.db import models

# Create your models here.

class Client(models.Model):

    name = models.CharField(max_length=160)

    def get_history_values(self):

        client_oportunities = self.opportunities.all()
        value_matrix = []
        for opportunity in client_oportunities:
            value_matrix.append(opportunity.get_history_values(365))
        return np.sum(value_matrix,axis=1).tolist()    

class Manager(models.Model):

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='managers')
    first_name = models.CharField(max_length=160)
    last_name = models.CharField(max_length=160)
    title = models.CharField(max_length=160)
    email = models.CharField(max_length=160)
    phone = models.CharField(max_length=160)
    address = models.CharField(max_length=160)