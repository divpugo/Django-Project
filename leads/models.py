from django.db import models
from django.db.models.signals import post_save, pre_delete  
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.apps import apps

#User class extends the AbstractUser model and includes additional role fields
class User(AbstractUser):
    is_organisor = models.BooleanField(default=True) #Organisor role
    is_agent = models.BooleanField(default=False) #Agent role
    is_lead = models.BooleanField(default=False) #Lead role

#UserProfile class with one-to-one relationship to User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

#Lead class with various fields and relationships to other models
class Lead(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    age = models.IntegerField(default=0)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    
    def __str__(self):
        if self.user is None:
            return f"Lead with ID {self.id} (No User)"
        return f"{self.user.first_name} {self.user.last_name}"

#Pre-delete signal for Lead class
@receiver(pre_delete, sender=Lead)
def pre_lead_delete(sender, instance, **kwargs):
    Apartment = apps.get_model('properties', 'Apartment')
    try:
        apartment = instance.apartment
        apartment.lead = None
        apartment.is_occupied = False
        apartment.save()
    except Apartment.DoesNotExist:
        pass
    
#Agent class with one-to-one relationship to User and foreign key to UserProfile
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

#Category class with foreign key to UserProfile
class Category(models.Model):
    name = models.CharField(max_length=30)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

#Signal to create a UserProfile upon User creation
def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)

#MaintenanceRequest class with various fields and relationships to other models
class MaintenanceRequest(models.Model):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (IN_PROGRESS, "In Progress"),
        (RESOLVED, "Resolved"),
    ]

    lead = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='maintenance_requests')
    apartment = models.ForeignKey("properties.Apartment", on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default=PENDING,
    )

    def __str__(self):
        return f"{self.lead} - {self.apartment} - {self.status}"

    @property
    def apartment_model(self):
        Apartment = apps.get_model('properties', 'Apartment')
        return Apartment.objects.get(pk=self.apartment_id)