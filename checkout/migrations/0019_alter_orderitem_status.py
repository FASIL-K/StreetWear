# Generated by Django 4.2.3 on 2023-08-05 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0018_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Processing', 'Processing'), ('Return', 'Return'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Pending', 'Pending')], default='Pending', max_length=150),
        ),
    ]
