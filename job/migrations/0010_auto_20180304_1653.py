# Generated by Django 2.0.2 on 2018-03-04 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0009_auto_20180304_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='student',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='application',
            name='trondheim',
            field=models.BooleanField(default=False),
        ),
    ]
