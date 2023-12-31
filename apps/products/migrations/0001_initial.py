# Generated by Django 4.2.7 on 2023-11-24 06:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Sets creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Sets the data update date')),
                ('name', models.CharField(max_length=255)),
                ('img', models.ImageField(null=True, upload_to='')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'category',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ProductAttachments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Sets creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Sets the data update date')),
                ('attachment', models.ImageField(upload_to='products/attachments')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Sets creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Sets the data update date')),
                ('name', models.CharField(max_length=255)),
                ('img', models.ImageField(null=True, upload_to='')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category')),
            ],
            options={
                'verbose_name': 'subcategory',
                'verbose_name_plural': 'subcategories',
                'db_table': 'sub_category',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Sets creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Sets the data update date')),
                ('deleted_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('details', models.TextField(default=None, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('discount', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)])),
                ('composition', models.CharField(max_length=255, null=True)),
                ('sub_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.subcategory')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': 'product',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Sets creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Sets the data update date')),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('text', models.TextField(default=None, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='products.products')),
            ],
            options={
                'verbose_name': 'review',
                'verbose_name_plural': 'reviews',
                'db_table': 'product_review',
                'ordering': ['-id'],
            },
        ),
    ]
