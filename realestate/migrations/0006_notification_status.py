# Generated by Django 3.2.8 on 2023-06-09 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0005_alter_notification_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]