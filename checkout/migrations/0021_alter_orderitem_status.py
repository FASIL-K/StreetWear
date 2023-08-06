# Generated by Django 4.2.3 on 2023-08-06 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0020_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Return', 'Return'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Processing', 'Processing'), ('Shipped', 'Shipped')], default='Pending', max_length=150),
        ),
    ]
