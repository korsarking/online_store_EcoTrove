# Generated by Django 4.2.7 on 2023-11-15 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Sets creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Sets the data update date')),
                ('country', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('block', models.CharField(max_length=10)),
                ('zipcode', models.CharField(max_length=16)),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
                'db_table': 'addresses',
                'ordering': ['-id'],
            },
        ),
    ]