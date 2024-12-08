from django.db import models

# Create your models here.
# class CO2(models.Model):
#     date = models.DateField()
#     average = models.FloatField()
    
#     class Meta:
#         ordering = ("date",)



# Codigo de inicio
# from django.db import models

# class AccessLog(models.Model):
#     timestamp = models.DateTimeField()
#     service_name = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.service_name} accessed on {self.timestamp}"




# Atual:
from django.db import models

class AccessLog(models.Model):
    # Defina as opções válidas para service_name
    SERVICE_CHOICES = [
        ('Home', 'Home'),
        ('Dashboard', 'Dashboard'),
        ('Profile', 'Profile'),
        ('Settings', 'Settings'),
        ('Reports', 'Reports'),
        ('Teste', 'Teste'),  # Adicionado o 'Teste' como você sugeriu
    ]

    timestamp = models.DateTimeField()
    service_name = models.CharField(max_length=100, choices=SERVICE_CHOICES)

    def __str__(self):
        return f"{self.service_name} accessed on {self.timestamp}"

