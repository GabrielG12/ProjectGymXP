# Generated by Django 4.2.2 on 2023-07-06 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0002_remove_training_type_training_quantity_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='time_type',
            field=models.CharField(blank=True, choices=[('Seconds', 'Seconds'), ('Minutes', 'Minutes'), ('Hours', 'Hours')], max_length=30, null=True),
        ),
    ]
