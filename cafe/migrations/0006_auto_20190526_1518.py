# Generated by Django 2.2 on 2019-05-26 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0005_menu_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='cafe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cafe.Cafe'),
        ),
    ]
