# Generated by Django 4.2.13 on 2024-06-29 11:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0002_sell'),
    ]

    operations = [
        migrations.AddField(
            model_name='sell',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
