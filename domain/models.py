from django.db import models

# Create your models here.
class Domain(models.Model):

    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to = 'logos/', default = 'logos/no-logo.png')

    def get_history_values(self):

        domain_oportunities = self.opportunities.all()
        value_matrix = []
        for opportunity in domain_oportunities:
            value_matrix.append(opportunity.get_history_values(365))
        return np.sum(value_matrix,axis=1).tolist()