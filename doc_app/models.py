from django.db import models

# Create your models here.
class Employees(models.Model):
    UserName = models.CharField(max_length=200)
    Password = models.CharField(max_length=200)