# Generated by Django 3.2.8 on 2023-06-15 22:51

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0010_alter_property_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(upload_to='profile_images'),
        ),
    ]
