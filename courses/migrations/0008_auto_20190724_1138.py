# Generated by Django 2.2.1 on 2019-07-24 11:38

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20190702_1750'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enrolled',
            options={'verbose_name': 'Enrollment', 'verbose_name_plural': 'Enrollments'},
        ),
        migrations.AlterField(
            model_name='enrolled',
            name='current_module',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='course', chained_model_field='course', null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.Modules'),
        ),
    ]
