# Generated by Django 5.0.7 on 2024-12-10 21:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0015_department_unique_department_organization_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='associatedetail',
            name='department',
        ),
        migrations.AlterField(
            model_name='department',
            name='description',
            field=models.TextField(verbose_name='Category description'),
        ),
        migrations.AlterField(
            model_name='department',
            name='hod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='hod_of', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Category Name'),
        ),
        migrations.AlterField(
            model_name='department',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='enterprise.organization'),
        ),
    ]