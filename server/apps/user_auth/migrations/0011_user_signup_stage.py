# Generated by Django 5.0.7 on 2024-10-07 12:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0010_stages'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='signup_stage',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='user_auth.stages'),
            preserve_default=False,
        ),
    ]