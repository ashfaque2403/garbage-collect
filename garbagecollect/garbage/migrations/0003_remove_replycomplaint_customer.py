# Generated by Django 4.2.9 on 2024-01-23 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garbage', '0002_replycomplaint'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='replycomplaint',
            name='customer',
        ),
    ]