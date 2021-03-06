from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('weight', models.IntegerField(default=100)),
            ],
            options={
                'verbose_name': 'gang',
                'verbose_name_plural': 'gangs',
                'ordering': ['weight'],
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=20000)),
                ('comment', models.TextField(blank=True, default='', max_length=100)),
                ('weight', models.IntegerField(default=100)),
                ('contact_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='position', to=settings.AUTH_USER_MODEL)),
                ('gang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='positions', to='jobs.Gang')),
                ('interviewers', models.ManyToManyField(blank=True, related_name='positions', to='accounts.Interviewer')),
            ],
            options={
                'verbose_name': 'position',
                'verbose_name_plural': 'positions',
                'ordering': ['weight'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('information', models.TextField(max_length=20000)),
                ('leader', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'section',
                'verbose_name_plural': 'sections',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='gang',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gangs', to='jobs.Section'),
        ),
    ]