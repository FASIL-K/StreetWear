# Generated by Django 4.2.3 on 2023-07-26 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='order_note',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
