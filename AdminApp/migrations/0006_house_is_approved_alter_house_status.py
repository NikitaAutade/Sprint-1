# Generated by Django 5.2.1 on 2025-05-27 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0005_alter_house_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='house',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Booked', 'Booked')], default='Available', max_length=50),
        ),
    ]
