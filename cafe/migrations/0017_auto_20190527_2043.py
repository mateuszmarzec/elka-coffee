# Generated by Django 2.2 on 2019-05-27 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0016_auto_20190527_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productingredient',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='storagestate',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
