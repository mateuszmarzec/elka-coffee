# Generated by Django 2.2 on 2019-05-27 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0015_auto_20190527_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cafe.OrderStatus'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cafe.PaymentType'),
        ),
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', to='cafe.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='storagestate',
            unique_together={('shop', 'ingredient')},
        ),
    ]