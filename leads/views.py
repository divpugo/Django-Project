from django.shortcuts import render, reverse, get_object_or_404
from agents.mixins import OrganisorAndLoginRequiredMixin
from .mixins import LeadRequiredMixin
from django.views import generic
from django.db.models import Count
from .models import Lead, Category, MaintenanceRequest
from properties.models import Apartment
from .forms import ( LeadModelForm, CustomUserCreationForm, 
    AssignAgentForm, LeadCategoryUpdateForm, CategoryModelForm, 
    MaintenanceRequestForm, MaintenanceRequestUpdateForm
)
from django.db.models import Q
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from .utils.qr_code_generator import generate_qr_code
from django.http import FileResponse


class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_lead:
                return reverse("leads:lead-dashboard")
            else:
                return reverse("leads:lead-list")

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("leads:login")

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"
    
    
class LeadListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    template_name = "leads/leads.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile).exclude(Q(agent__isnull=True) | Q(apartment__isnull=True))


    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            all_leads = Lead.objects.filter(organisation=user.userprofile)
            leads_with_apartments = Apartment.objects.filter(lead__in=all_leads).values_list('lead', flat=True)
            queryset = all_leads.filter(Q(agent__isnull=True) | Q(apartment__isnull=True))
            context.update({
                "unassigned_leads": queryset
            })
        return context

class LeadDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"
    
    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset
    
class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        return super(LeadCreateView, self).form_valid(form)



class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)
    
    def get_success_url(self):
        referer_url = self.request.headers.get('Referer')
        pk = referer_url.split("/")[-3]
        return reverse("leads:lead-detail", kwargs={"pk":pk})
    
class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('leads:lead-list')
    
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

        
class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        apartment = form.cleaned_data["apartment"]
        lead = get_object_or_404(Lead, id=self.kwargs["pk"])
        apartment.lead = lead
        apartment.is_occupied = True
        apartment.save()
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lead = get_object_or_404(Lead, id=self.kwargs["pk"])
        context['lead'] = lead
        return context
        
class CategoryListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    model = Category
    template_name = 'leads/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(num_leads=Count('leads'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            leads = Lead.objects.filter(
                organisation=user.userprofile
            )
        else:
            leads = Lead.objects.filter(
                organisation=user.agent.organisation
            )
        unassigned_lead_count = leads.filter(category__isnull=True).count()

        categories = context['categories']
        category_lead_counts = leads.filter(category__in=categories).values('category').annotate(count=Count('category'))

        context['unassigned_lead_count'] = unassigned_lead_count
        context['category_lead_counts'] = []

        for category in categories:
            count = 0
            for category_lead_count in category_lead_counts:
                if category == category_lead_count['category']:
                    count = category_lead_count['count']
                    break
            context['category_lead_counts'].append(count)

        return context

            
class CategoryDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"     
    context_object_name = "category"
        
    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset
    
class LeadCategoryUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})

class CategoryCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/category_create.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse('leads:category-list')
    
    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)

class CategoryUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/category_update.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class CategoryDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/category_delete.html"

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset
        
class LeadDashboardView(LeadRequiredMixin, generic.TemplateView):
    template_name = "leads/tenant_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lead = self.request.user.lead
        context['category'] = lead.category
        try:
            context['apartment'] = lead.apartment
        except Apartment.DoesNotExist:
            context['apartment'] = None
        return context
    
class MaintenanceRequestCreateView(LeadRequiredMixin, generic.CreateView):
    model = MaintenanceRequest
    form_class = MaintenanceRequestForm
    template_name = "leads/maintenance_request_create.html"

    def form_valid(self, form):
        form.instance.lead = self.request.user
        response = super().form_valid(form)
        
        # Send email to the lead's agent and the agent's organizer
        lead_name = self.request.user.get_full_name()
        apartment_name = form.instance.apartment.name
        description = form.instance.description
        agent_email = self.request.user.lead.agent

        email_message = (
            f"Dear Agent,\n\n"
            f"A maintenance request has been raised for the apartment {apartment_name}.\n\n"
            f"Description of the request: {description}\n\n"
            "Best regards,\n"
            "Your Management Team"
        )

        send_mail(
            subject=f'Maintenance Request for {apartment_name} by {lead_name}',
            message=email_message,
            from_email="test@test.com",
            recipient_list=[agent_email],
            fail_silently=False
        )

        return response

    def get_success_url(self):
        return reverse("leads:lead-dashboard")
    
class MaintenanceRequestListView(LeadRequiredMixin, generic.ListView):
    model = MaintenanceRequest
    context_object_name = "maintenance_requests"
    template_name = "leads/maintenance_request_list.html"

    def get_queryset(self):
        return MaintenanceRequest.objects.filter(lead=self.request.user)

class MaintenanceRequestUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    model = MaintenanceRequest
    form_class = MaintenanceRequestUpdateForm
    template_name = "leads/maintenance_request_update.html"

    def get_queryset(self):
        queryset = MaintenanceRequest.objects.all()
        if self.request.user.is_agent:
            queryset = queryset.filter(lead__agent=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse("leads:maintenance_request_display")

class MaintenanceRequestDisplayView(OrganisorAndLoginRequiredMixin, generic.ListView):
    model = MaintenanceRequest
    context_object_name = "maintenance_requests"
    template_name = "leads/maintenance_request_display.html"

    def get_queryset(self):
        return MaintenanceRequest.objects.all().select_related('lead', 'apartment')

    
def lead_category_qr_code(request, lead_id):
    lead = Lead.objects.get(id=lead_id)
    category_id = lead.category.id
    category_url = request.build_absolute_uri(reverse('leads:category_qr_code_detail', args=[category_id]))
    qr_code_image = generate_qr_code(category_url)
    return FileResponse(qr_code_image, content_type='image/png')

def category_qr_code_detail(request, pk):
    category = Category.objects.get(pk=pk)
    context = {'category': category}
    return render(request, 'leads/category_qr_code_detail.html', context)

