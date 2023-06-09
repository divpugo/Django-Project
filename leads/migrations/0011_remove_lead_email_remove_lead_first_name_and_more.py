# Generated by Django 4.2 on 2023-04-23 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0010_lead_date_added_lead_description_lead_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='email',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='lead',
            name='last_name',
        ),
        migrations.AddField(
            model_name='lead',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
