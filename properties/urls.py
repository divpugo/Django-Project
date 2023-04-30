from django.urls import path
from .views import (
    PropertyListView, PropertyCreateView, ApartmentCreateView, 
    PropertyDetailView, UtilityCreateView, UtilityUpdateView, UtilityListView,
    UtilityDetailView, BillCreateView, BillDetailView, ApartmentDetailView,
    ApartmentUpdateView,
)

app_name = "properties"

urlpatterns = [
    path('', PropertyListView.as_view(), name='property-list'),
    path('create/', PropertyCreateView.as_view(), name='property-create'),
    path('<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    path('create-apartment/', ApartmentCreateView.as_view(), name='apartment-create'),
    path('utilities/detail/<int:property_id>/<int:utility_pk>/', UtilityDetailView.as_view(), name='utility_detail_list'),
    path('utility/list/<int:property_id>/', UtilityListView.as_view(), name='utility-list'),
    path('utilities/create/', UtilityCreateView.as_view(), name='utility_create'),
    path('utilities/<int:pk>/update/', UtilityUpdateView.as_view(), name='utility_update'),
    path('utilities/<int:utility_id>/bills/create/', BillCreateView.as_view(), name='bill_create'),
    path('bills/<int:pk>/', BillDetailView.as_view(), name='bill_detail'),
    path('apartment/<int:pk>/', ApartmentDetailView.as_view(), name='apartment-detail'),
    path('apartment/<int:pk>/update/', ApartmentUpdateView.as_view(), name='apartment-update'),

]
