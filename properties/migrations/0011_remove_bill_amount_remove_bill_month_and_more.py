# Generated by Django 4.2 on 2023-04-24 20:16

from django.db import migrations, models
import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0010_remove_utility_image_bill'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='month',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='year',
        ),
        migrations.AddField(
            model_name='bill',
            name='date',
            field=models.DateField(default=datetime.date(2020, 11, 1)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bill',
            name='total',
            field=models.DecimalField(decimal_places=2, default='12.00', max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bill',
            name='unit',
            field=models.IntegerField(default='0'),
            preserve_default=False,
        ),
    ]
