# Generated by Django 2.2.6 on 2019-11-02 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20191102_0558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='flavour',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
