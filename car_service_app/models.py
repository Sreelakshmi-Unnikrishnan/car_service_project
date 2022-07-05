from operator import mod
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from froala_editor.fields import FroalaField

# Create your models here.

class Service(models.Model):
    service_name = models.CharField(max_length=30)
    service_details = models.CharField(max_length=30)
    service_rate = models.IntegerField(default=0)
    
    def __str__(self):
        return "ID: " + str(self.id) + " | Service Name: " + str(self.service_name)

class Buyer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=30)
    car_model = models.CharField(max_length=30)
    number_plate_no = models.CharField(max_length=30)
    service_name = models.ForeignKey(Service, on_delete=models.CASCADE)
    service_date = models.DateField()
