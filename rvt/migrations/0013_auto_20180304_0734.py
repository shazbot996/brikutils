# Generated by Django 2.0.2 on 2018-03-04 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rvt', '0012_auto_20180304_0645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rvtvinfo',
            name='rvt_vi_id',
            field=models.CharField(blank=True, default='UNSET', max_length=300, null=True),
        ),
    ]