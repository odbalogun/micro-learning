# Generated by Django 2.2.1 on 2019-05-30 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0003_auto_20190530_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modules',
            name='date_created',
        ),
        migrations.AddField(
            model_name='modules',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='modules',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_modules', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='enrolled',
            name='date_enrolled',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date enrolled'),
        ),
        migrations.AlterField(
            model_name='modules',
            name='access_code',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='media code'),
        ),
        migrations.AlterField(
            model_name='modules',
            name='order',
            field=models.IntegerField(verbose_name='position'),
        ),
    ]
