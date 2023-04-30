from django.contrib import admin
from .models import Property, Apartment, Bill

admin.site.register(Property)
admin.site.register(Apartment)
admin.site.register(Bill)
