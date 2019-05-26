# Generated by Django 2.2 on 2019-05-26 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0004_auto_20190525_1551'),
        ('users', '0007_auto_20190525_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='cafe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cafe.Cafe'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
