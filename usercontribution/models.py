from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now   

class UserContribution(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.OneToOneField("Source", on_delete=models.CASCADE)
    # source = models.CharField(max_length=266)
    
    def __str__(self):
        return f"{self.owner}, {self.amount}, {self.description}, {self.source}, {self.date}"
    
    class Meta:
        ordering = ['-date']
    
class Source(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    