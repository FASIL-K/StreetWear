# Generated by Django 4.2.3 on 2023-07-25 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='selected_size',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
