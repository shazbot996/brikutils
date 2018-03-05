# Generated by Django 2.0.2 on 2018-03-04 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rvt', '0016_rvtvpartition'),
    ]

    operations = [
        migrations.CreateModel(
            name='RVTvDatastore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rvt_vi_batch', models.IntegerField(null=True)),
                ('rvt_vs_name', models.CharField(blank=True, max_length=300, null=True)),
                ('rvt_vs_type', models.CharField(default='UNSET', max_length=300)),
                ('rvt_vs_vmcount', models.IntegerField(null=True)),
                ('rvt_vs_capacitymb', models.IntegerField(null=True)),
                ('rvt_vs_provisioinedmb', models.IntegerField(null=True)),
                ('rvt_vs_usedmb', models.IntegerField(null=True)),
                ('rvt_vs_freemb', models.IntegerField(null=True)),
                ('load_time', models.DateTimeField(auto_now_add=True)),
                ('last_edit', models.DateTimeField(auto_now=True)),
                ('rvt_vs_user', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='rvt_vs_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
