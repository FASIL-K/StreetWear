# Generated by Django 4.2.3 on 2023-08-03 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_size_product_sizes'),
    ]

    operations = [
        migrations.CreateModel(
            name='price_range',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('low', models.IntegerField()),
                ('high', models.IntegerField()),
            ],
        ),
    ]
