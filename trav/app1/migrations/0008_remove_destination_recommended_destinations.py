# Generated by Django 5.1.7 on 2025-03-11 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_destination_recommended_destinations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='destination',
            name='recommended_destinations',
        ),
    ]
