# Generated by Django 4.2.2 on 2023-07-05 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exercises',
            old_name='type',
            new_name='exercise_type',
        ),
    ]
