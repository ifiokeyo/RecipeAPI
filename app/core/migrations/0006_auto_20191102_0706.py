# Generated by Django 2.2.6 on 2019-11-02 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20191102_0650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='flavour',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
