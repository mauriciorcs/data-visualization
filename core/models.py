from django.db import models

# Create your models here.
# class CO2(models.Model):
#     date = models.DateField()
#     average = models.FloatField()
    
#     class Meta:
#         ordering = ("date",)

from django.db import models

class AccessLog(models.Model):
    timestamp = models.DateTimeField()
    service_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.service_name} accessed on {self.timestamp}"
