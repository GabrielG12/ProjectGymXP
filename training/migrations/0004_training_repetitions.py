# Generated by Django 4.2.2 on 2023-07-06 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0003_training_time_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='repetitions',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]