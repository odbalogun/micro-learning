# Generated by Django 2.2.1 on 2019-07-24 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_auto_20190724_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrolled',
            name='status',
            field=models.CharField(choices=[('ongoing', 'Ongoing'), ('completed', 'Completed')], default='ongoing', max_length=50),
        ),
    ]