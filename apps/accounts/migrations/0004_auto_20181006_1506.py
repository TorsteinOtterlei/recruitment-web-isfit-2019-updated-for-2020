# Generated by Django 2.0.2 on 2018-10-06 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20181004_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('NE', 'Not evaluated'), ('IS', 'Interview set'), ('IC', 'Interview confirmed'), ('ID', 'Interviewed'), ('NM', 'Not met'), ('AC', 'Accepted'), ('PP', 'Possibly participant'), ('AW', 'Application Withdrawn')], default='NE', max_length=2),
        ),
    ]
