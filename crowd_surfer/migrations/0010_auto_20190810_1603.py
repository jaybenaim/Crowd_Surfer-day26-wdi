# Generated by Django 2.2.3 on 2019-08-10 16:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowd_surfer', '0009_merge_20190809_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='category',
            field=models.CharField(default='Random', max_length=63),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='backers',
            field=models.ManyToManyField(related_name='projects_backed', to=settings.AUTH_USER_MODEL),
        ),
    ]