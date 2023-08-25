# Generated by Django 4.2.3 on 2023-08-25 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0035_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Return', 'Return'), ('Cancelled', 'Cancelled'), ('Pending', 'Pending'), ('Processing', 'Processing'), ('Delivered', 'Delivered'), ('Shipped', 'Shipped')], default='Pending', max_length=150),
        ),
    ]