# Generated by Django 4.2 on 2023-04-24 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0013_remove_lead_apartment'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='is_organisor',
            field=models.BooleanField(default=False),
        ),
    ]