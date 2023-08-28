# Generated by Django 4.2.3 on 2023-08-28 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0040_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Processing', 'Processing'), ('Return', 'Return'), ('Pending', 'Pending'), ('Shipped', 'Shipped')], default='Pending', max_length=150),
        ),
    ]