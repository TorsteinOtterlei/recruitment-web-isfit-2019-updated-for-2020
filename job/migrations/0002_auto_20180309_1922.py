# Generated by Django 2.0.2 on 2018-03-09 18:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='interview_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]