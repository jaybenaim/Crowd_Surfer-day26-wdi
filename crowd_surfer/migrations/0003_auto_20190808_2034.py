# Generated by Django 2.2.3 on 2019-08-08 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowd_surfer', '0002_project_funding_goal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='funding_goal',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='reward',
            name='reward_amount',
            field=models.PositiveIntegerField(),
        ),
    ]
