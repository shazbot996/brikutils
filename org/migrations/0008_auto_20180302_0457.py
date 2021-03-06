# Generated by Django 2.0.2 on 2018-03-02 04:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0007_auto_20180302_0452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='org',
            name='org_contact',
            field=models.CharField(max_length=300, verbose_name='Contact'),
        ),
        migrations.AlterField(
            model_name='org',
            name='org_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='org_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='org',
            name='org_email',
            field=models.EmailField(max_length=254, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='org',
            name='org_name',
            field=models.CharField(max_length=300, verbose_name='Name'),
        ),
    ]
