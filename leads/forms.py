from django import forms
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Lead, Agent, Category, MaintenanceRequest
from properties.models import Apartment
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail

User = get_user_model()

#LeadModelForm: A form for creating new Lead instances
class LeadModelForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    apartment = forms.ModelChoiceField(queryset=Apartment.objects.filter(is_occupied=False), required=False)

    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
            'description',
            'phone_number',
            'email',
        )

    # Validate email field
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise ValidationError("This email is already taken as a username.")
        return email
    
    # Validate username field
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    # Save the Lead instance and related User instance
    def save(self, commit=True):
        lead = super().save(commit=False)
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        password = User.objects.make_random_password()

        if commit:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_organisor=False,  
                is_lead=True
            )
            user.groups.add(Group.objects.get(name='leads'))
            lead.user = user

            apartment = self.cleaned_data['apartment']
            if apartment:
                apartment.is_occupied = True
                apartment.lead = lead  
                apartment.save()

            lead.save()
            
            #Send mail notification when lead is created
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_password_url = f"http://127.0.0.1:8000/password-reset-confirm/{uid}/{token}/"
            
            user = lead.user

            email_message = (
                f"Dear {user.first_name},\n\n"
                "A new tenant account has been created for you. "
                "Please use the following credentials to log in:\n\n"
                f"Username: {user.username}\n"
                f"Password: {user.password}\n\n"  # Use the raw password from the user object
                "For security reasons, we recommend resetting your password. "
                "Please go to the following URL to reset your password:\n\n"
                f"{reset_password_url}\n\n"
                "Best regards,\n"
                "Your Management Team"
            )

            send_mail(
                subject="New tenant",
                message=email_message,
                from_email="test@test.com",
                recipient_list=[user.email]
            )
        return lead

#CustomUserCreationForm: A form for creating new User instances
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {"username": UsernameField,
                         "email": forms.EmailField, }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

#AssignAgentForm: A form for assigning agents and apartments
class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())
    apartment = forms.ModelChoiceField(queryset=Apartment.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        available_apartments = Apartment.objects.filter(is_occupied=False)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents
        self.fields["apartment"].queryset = available_apartments

#LeadCategoryUpdateForm: A form for updating the category of a lead
class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category',
        )

#CategoryModelForm: A form for creating new Category instances        
class CategoryModelForm(forms.ModelForm):
    class Meta:
        model= Category
        fields = (
            'name',
        )

#MaintenanceRequestForm: A form for creating new MaintenanceRequest instances        
class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ('apartment', 'description')

#MaintenanceRequestUpdateForm: A form for updating MaintenanceRequest instances
class MaintenanceRequestUpdateForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['status', 'description']