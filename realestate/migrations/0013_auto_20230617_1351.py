# Generated by Django 3.2.8 on 2023-06-17 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0012_alter_message_subject'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='state_lga',
            new_name='town',
        ),
        migrations.AlterField(
            model_name='property',
            name='bathroom_type',
            field=models.CharField(choices=[('Self-contained', 'Self-contained'), ('General', 'General'), ('Private Detached', 'Private Detached')], max_length=60),
        ),
        migrations.AlterField(
            model_name='property',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_type',
            field=models.CharField(choices=[('Complete House', 'Complete House'), ('One Room Apartment', 'One Room Apartment'), ('Bedroom & Palour', 'Bedroom & Palour'), ('Bedroom & Palour Self-Contained', 'Bedroom & Palour Self-Contained'), ('One Room Self-Contained', 'One Room Self-Contained')], max_length=100),
        ),
    ]
