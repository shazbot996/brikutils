# Generated by Django 2.0.2 on 2018-02-27 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rvt', '0008_auto_20180227_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rvtvinfo',
            name='org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.Org'),
        ),
    ]
