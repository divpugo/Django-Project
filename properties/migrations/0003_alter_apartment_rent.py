# Generated by Django 4.2 on 2023-04-23 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0002_remove_property_agent_apartment_agent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='rent',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
    ]
