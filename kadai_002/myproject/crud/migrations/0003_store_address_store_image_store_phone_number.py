# Generated by Django 5.0.3 on 2024-04-08 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0002_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='address',
            field=models.CharField(blank=True, default='Tokyo, Japan', max_length=200),
        ),
        migrations.AddField(
            model_name='store',
            name='image',
            field=models.ImageField(default='default_image.jpg', upload_to='store_images/'),
        ),
        migrations.AddField(
            model_name='store',
            name='phone_number',
            field=models.CharField(default='', max_length=20),
        ),
    ]