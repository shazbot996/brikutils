# Generated by Django 2.0.2 on 2018-03-05 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rvt', '0019_auto_20180304_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='rvtvinfo',
            name='rvt_vi_sdkserver',
            field=models.CharField(blank=True, default='UNSET', max_length=300, null=True),
        ),
    ]