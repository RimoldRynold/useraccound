# Generated by Django 3.2.9 on 2021-12-09 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='threshold',
            name='flag',
            field=models.BooleanField(default=False),
        ),
    ]
