# Generated by Django 3.2.9 on 2021-12-09 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_threshold_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threshold',
            name='value',
            field=models.IntegerField(),
        ),
    ]
