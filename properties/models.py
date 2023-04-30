from django.db import models
from leads.models import UserProfile, Agent
import datetime

class Property(models.Model):
    name = models.CharField(max_length=100)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='properties/', default='default_property.jpg')

    def __str__(self):
        return self.name

class Apartment(models.Model):
    property = models.ForeignKey(Property, related_name='apartments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_occupied = models.BooleanField(default=False)
    lead = models.OneToOneField('leads.Lead', null=True, blank=True, on_delete=models.SET_NULL)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    rent = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='apartments/', default='default_apartment.jpg')
        
    def __str__(self):
        return f"{self.property.name} - {self.name}"

class Utility(models.Model):
    property = models.ForeignKey(Property, related_name='utilities', on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, related_name='utilities', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Bill(models.Model):
    utility = models.ForeignKey(Utility, related_name='bills', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='bills/', default='default_bill.jpg')
    date = models.DateField(default=datetime.date(2020, 11, 1))

    def __str__(self):
        return f"{self.utility.name} - {self.date}"
