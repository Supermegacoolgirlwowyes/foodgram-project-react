# Generated by Django 3.1.14 on 2022-01-27 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_customtoken'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomToken',
        ),
    ]