# Generated by Django 2.0.2 on 2018-03-02 05:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0008_auto_20180302_0457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='assess_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assess_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='assess_name',
            field=models.CharField(max_length=300, verbose_name='assess_name'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='assess_org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assess_org', to='org.Org'),
        ),
    ]
