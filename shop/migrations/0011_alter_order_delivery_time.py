# Generated by Django 5.1.1 on 2024-09-23 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_consultationrequest_message_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_time',
            field=models.CharField(blank=True, choices=[('01', 'Как можно скорее'), ('02', '10:00-12:00'), ('03', '12:00-14:00'), ('04', '14:00-16:00'), ('05', '16:00-18:00'), ('06', '18:00-20:00')], default='01', max_length=2, verbose_name='время доставки'),
        ),
    ]
