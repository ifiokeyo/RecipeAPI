# Generated by Django 2.2.6 on 2019-11-02 04:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_pizza'),
    ]
    operations = [
        migrations.RunSQL(
            'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";',
        ),
    ]
