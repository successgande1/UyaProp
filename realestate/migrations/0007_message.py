# Generated by Django 3.2.8 on 2023-06-09 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0006_notification_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(choices=[('Inquiry', 'Inquiry'), ('Reinquiry', 'Reinquiry'), ('Payment', 'Payment')], max_length=20)),
                ('message', models.TextField(blank=True, max_length=220, null=True)),
                ('status', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestate.property')),
                ('prospect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestate.prospect')),
            ],
        ),
    ]