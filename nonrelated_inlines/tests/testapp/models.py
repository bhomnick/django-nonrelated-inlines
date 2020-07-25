from django.db import models


class Customer(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)


class Invoice(models.Model):
    email = models.EmailField()
    amount = models.IntegerField()
