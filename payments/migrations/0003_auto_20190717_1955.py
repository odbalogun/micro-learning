# Generated by Django 2.2.1 on 2019-07-17 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_remove_paymentlog_enrolled'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymentlog',
            options={'verbose_name': 'payment', 'verbose_name_plural': 'payments'},
        ),
    ]