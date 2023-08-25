# Generated by Django 4.2.3 on 2023-08-25 17:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(max_length=100)),
                ('discount_amount', models.PositiveIntegerField()),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
    ]
