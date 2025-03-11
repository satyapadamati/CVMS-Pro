from django.db import models
from django.contrib.auth.models import User

# Minimal model for Django auth compatibility; actual data in DynamoDB

from django.db import models

class Vehicle(models.Model):
    vehicle_id = models.CharField(max_length=36, primary_key=True)
    user_id = models.CharField(max_length=100)
    vehicle_name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()

class MaintenanceRecord(models.Model):
    record_id = models.CharField(max_length=36, primary_key=True)
    vehicle_id = models.CharField(max_length=36)
    service_date = models.DateField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)