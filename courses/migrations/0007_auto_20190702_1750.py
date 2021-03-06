# Generated by Django 2.2.1 on 2019-07-02 17:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20190629_1118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enrolled',
            name='amount_paid',
        ),
        migrations.AddField(
            model_name='enrolled',
            name='current_module',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.Modules'),
        ),
        migrations.AlterField(
            model_name='courses',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_courses', to=settings.AUTH_USER_MODEL),
        ),
    ]
