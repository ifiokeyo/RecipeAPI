# Generated by Django 2.2.6 on 2019-11-04 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_pizza_prices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('I', 'In-progress'), ('C', 'Cancelled'), ('DN', 'Done'), ('DL', 'Delivered')], default='P', max_length=2),
        ),
    ]