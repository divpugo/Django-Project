from django.urls import path
from .views import (LeadListView, LeadDetailView, LeadCreateView, 
    LeadUpdateView, LeadDeleteView, AssignAgentView,
    CategoryListView, CategoryDetailView, LeadCategoryUpdateView,
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    LeadDashboardView, CustomLoginView, MaintenanceRequestCreateView,
    MaintenanceRequestListView, MaintenanceRequestUpdateView,
    category_qr_code_detail, lead_category_qr_code, MaintenanceRequestDisplayView,
)

app_name = "leads"
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name="login"),
    path('', LeadListView.as_view(), name='lead-list'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
    path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('create-category/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/update', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete', CategoryDeleteView.as_view(), name='category-delete'),
    path('dashboard/', LeadDashboardView.as_view(), name='lead-dashboard'),
    path('maintenance-request/create/', MaintenanceRequestCreateView.as_view(), name='maintenance-request-create'),
    path('maintenance_request/list/', MaintenanceRequestListView.as_view(), name='maintenance_request_list'),
    path('maintenance_request/update/<int:pk>/', MaintenanceRequestUpdateView.as_view(), name='maintenance_request_update'),
    path('maintenance_request/display/', MaintenanceRequestDisplayView.as_view(), name='maintenance_request_display'),
    path('category_qr_code_detail/<int:pk>/', category_qr_code_detail, name='category_qr_code_detail'),
    path('lead/<int:lead_id>/qr-code/', lead_category_qr_code, name='lead-category-qr-code'),
]
