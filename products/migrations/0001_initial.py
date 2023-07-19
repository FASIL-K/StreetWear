# Generated by Django 4.2.3 on 2023-07-18 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0003_brand'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(upload_to='media/products')),
                ('image2', models.ImageField(upload_to='media/products')),
                ('image3', models.ImageField(upload_to='media/products')),
                ('product_name', models.CharField(max_length=50, unique=True)),
                ('product_price', models.IntegerField()),
                ('stock', models.PositiveIntegerField()),
                ('product_description', models.TextField(blank=True)),
                ('is_available', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
        ),
    ]
