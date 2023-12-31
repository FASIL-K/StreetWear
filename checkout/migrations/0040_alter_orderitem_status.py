# Generated by Django 4.2.3 on 2023-08-28 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0039_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Pending', 'Pending'), ('Return', 'Return'), ('Cancelled', 'Cancelled')], default='Pending', max_length=150),
        ),
    ]
