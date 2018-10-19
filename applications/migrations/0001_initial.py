from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=2000)),
                ('withdrawn', models.BooleanField(default=False)),
                ('applicant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='application', to='accounts.Applicant')),
                ('first', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='first', to='jobs.Position')),
                ('second', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second', to='jobs.Position')),
                ('third', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='third', to='jobs.Position')),
            ],
        ),
    ]