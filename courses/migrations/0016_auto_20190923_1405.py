# Generated by Django 2.2.1 on 2019-09-23 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_courses_learning_and_outcome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='strategy',
            field=models.TextField(blank=True, null=True, verbose_name='course strategy'),
        ),
        migrations.AlterField(
            model_name='courses',
            name='tools_and_technology',
            field=models.TextField(blank=True, null=True, verbose_name='tools and Technologies'),
        ),
        migrations.AlterField(
            model_name='enrolled',
            name='payment_status',
            field=models.CharField(choices=[('unpaid', 'Unpaid'), ('partly', 'Part Payment'), ('paid', 'Fully Paid')], default='unpaid', max_length=50),
        ),
        migrations.AlterField(
            model_name='enrolled',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('ongoing', 'Ongoing'), ('completed', 'Completed')], default='pending', max_length=50),
        ),
    ]