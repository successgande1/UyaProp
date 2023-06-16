# Generated by Django 3.2.8 on 2023-06-15 21:39

from django.db import migrations, models
import realestate.models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0009_alter_property_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='image',
            field=models.ImageField(upload_to='profile_images', validators=[realestate.models.AllowedFormatsValidator()]),
        ),
    ]