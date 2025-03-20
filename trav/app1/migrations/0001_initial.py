# Generated by Django 5.1.5 on 2025-03-07 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('beach', 'Beach'), ('mountain', 'Mountain'), ('historical', 'Historical'), ('city', 'City'), ('adventure', 'Adventure')], max_length=100)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('map_link', models.URLField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='destination/')),
            ],
        ),
    ]
