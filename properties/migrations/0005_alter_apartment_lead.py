# Generated by Django 4.2 on 2023-04-23 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0013_remove_lead_apartment'),
        ('properties', '0004_alter_apartment_lead'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='lead',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.lead'),
        ),
    ]