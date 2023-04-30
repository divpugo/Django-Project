from django.shortcuts import render, reverse,get_object_or_404
from django.views import generic
from .models import Property, Utility, Apartment, Bill
from .forms import PropertyModelForm, ApartmentModelForm, UtilityCreateForm, UtilityUpdateForm, BillModelForm
from agents.mixins import OrganisorAndLoginRequiredMixin
import os
import tempfile
from PIL import Image
from .receipt_scanner import extract_information, preprocess_image, extract_text, extract_information

class BillCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "properties/bill_create.html"
    form_class = BillModelForm

    def process_uploaded_image(self, image):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
            img = Image.open(image)
            img.save(temp_image, format='JPEG')
            temp_image.flush()
            temp_image.close()
            preprocessed_image = preprocess_image(temp_image.name)
            text = extract_text(preprocessed_image)
            extracted_data = extract_information(text)
            os.unlink(temp_image.name)
        return extracted_data

    def form_valid(self, form):
        utility = Utility.objects.get(pk=self.kwargs['utility_id'])
        form.instance.utility = utility

        image = self.request.FILES.get('image')
        if image:
            extracted_data = self.process_uploaded_image(image)
            form.instance.date = extracted_data['date'] if extracted_data['date'] else form.instance.date
            form.instance.amount = extracted_data['amount']

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('properties:bill_detail', kwargs={'pk': self.object.pk})

    
class BillDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    model = Bill
    template_name = 'properties/bill_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bill = self.get_object()

        context['date'] = bill.date
        context['amount'] = bill.amount

        return context


class PropertyListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = "properties/property_list.html"
    context_object_name = "properties"

    def get_queryset(self):
        return Property.objects.filter(organisation=self.request.user.userprofile)

class PropertyCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "properties/property_create.html"
    form_class = PropertyModelForm

    def get_success_url(self):
        return reverse('properties:property-list')

    def form_valid(self, form):
        property = form.save(commit=False)
        property.organisation = self.request.user.userprofile
        property.save()
        return super(PropertyCreateView, self).form_valid(form)

class PropertyDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "properties/property_detail.html"  # Fix the typo here
    context_object_name = "property"
    
    def get_queryset(self):
        return Property.objects.filter(organisation=self.request.user.userprofile)


class ApartmentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "properties/apartment_create.html"
    form_class = ApartmentModelForm

    def get_success_url(self):
        return reverse('properties:property-list')

    def form_valid(self, form):
        apartment = form.save(commit=False)
        apartment.save()
        return super(ApartmentCreateView, self).form_valid(form)

class UtilityCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    model = Utility
    form_class = UtilityCreateForm
    template_name = 'properties/utility_create.html'
        
    def get_success_url(self):
        return reverse('properties:utility-list', kwargs={'property_id': self.object.property.id})


class UtilityUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    model = Utility
    form_class = UtilityUpdateForm
    template_name = 'properties/utility_update.html'

    def get_success_url(self):
        return reverse('properties:utility_list', kwargs={'property_id': self.object.property.id})

class UtilityListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    model = Utility
    template_name = 'properties/utility_list.html'
    context_object_name = 'utilities'

    def get_queryset(self):
        property_id = self.kwargs['property_id']
        return Utility.objects.filter(property_id=property_id)
    
class UtilityDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    model = Utility
    template_name = 'properties/utility_detail_list.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Utility, property_id=self.kwargs['property_id'], pk=self.kwargs['utility_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bills'] = Bill.objects.filter(utility=self.object)
        return context

class ApartmentDetailView(generic.DetailView):
    model = Apartment
    template_name = "properties/apartment_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ApartmentModelForm(instance=self.object)
        return context
    
class ApartmentUpdateView(generic.UpdateView):
    model = Apartment
    form_class = ApartmentModelForm
    template_name = 'properties/apartment_update.html'

    def get_success_url(self):
        return reverse('properties:apartment-detail', kwargs={'pk': self.object.property.pk})