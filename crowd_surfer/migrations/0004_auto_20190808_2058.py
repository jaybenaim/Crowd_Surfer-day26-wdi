# Generated by Django 2.2.3 on 2019-08-08 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowd_surfer', '0003_auto_20190808_2034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reward',
            name='reward_type',
        ),
        migrations.AddField(
            model_name='reward',
            name='reward_description',
            field=models.TextField(null=True),
        ),
    ]