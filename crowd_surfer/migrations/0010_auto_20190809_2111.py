# Generated by Django 2.2.4 on 2019-08-09 21:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowd_surfer', '0009_merge_20190809_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='backers',
            field=models.ManyToManyField(related_name='projects_backed', to=settings.AUTH_USER_MODEL),
        ),
    ]
