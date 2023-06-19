# Generated by Django 3.2.8 on 2023-06-19 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.CharField(blank=True, max_length=35, null=True)),
                ('subject', models.CharField(choices=[('Inquiry', 'Inquiry')], max_length=20)),
                ('phone', models.CharField(blank=True, max_length=11, null=True)),
                ('content', models.TextField(blank=True, max_length=220, null=True)),
                ('status', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
