# Generated by Django 5.0.7 on 2025-01-01 21:33

import apps.user_auth.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0016_alter_agent_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profile_image',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='agent',
            name='bio',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='agent',
            name='first_name',
            field=models.CharField(default='fill', max_length=150, verbose_name='first name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agent',
            name='last_name',
            field=models.CharField(default='put', max_length=150, verbose_name='last name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agent',
            name='phone_number',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AddField(
            model_name='agent',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=apps.user_auth.utils.profile_image_upload_location, verbose_name='user media uploads'),
        ),
        migrations.AddField(
            model_name='agent',
            name='username',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vendor',
            name='bio',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='phone_number',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=apps.user_auth.utils.profile_image_upload_location, verbose_name='user media uploads'),
        ),
        migrations.AddField(
            model_name='vendor',
            name='vendor_name',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]
