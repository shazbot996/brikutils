# Generated by Django 2.0.2 on 2018-02-27 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0002_auto_20180227_1733'),
    ]

    operations = [
        migrations.RenameField(
            model_name='org',
            old_name='last_vi_edit',
            new_name='last_edit',
        ),
        migrations.RenameField(
            model_name='org',
            old_name='load_vi_time',
            new_name='load_time',
        ),
    ]
