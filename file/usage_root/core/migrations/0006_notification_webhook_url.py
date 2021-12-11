# Generated by Django 3.2.9 on 2021-12-10 06:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_threshold_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='webhook_url',
            field=models.URLField(default=django.utils.timezone.now, max_length=250),
            preserve_default=False,
        ),
    ]