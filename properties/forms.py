from django import forms
from .models import Property, Apartment
from .models import Utility, Bill

class PropertyModelForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = (
            'name',
            'organisation',
            'location',
            'description',
            'image', 
        )

class ApartmentModelForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = (
            'property',
            'name',
            'is_occupied',
            'lead',
            'agent',
            'description',
            'rent',
            'image', 
        )

class UtilityCreateForm(forms.ModelForm):
    class Meta:
        model = Utility
        fields = ('property', 'apartment', 'name', 'description')
        widgets = {
            'property': forms.Select(attrs={'class': 'form-control'}),
            'apartment': forms.Select(attrs={'class': 'form-control'}),
        }

class UtilityUpdateForm(forms.ModelForm):
    class Meta:
        model = Utility
        fields = ('name', 'description')

class BillModelForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['image']