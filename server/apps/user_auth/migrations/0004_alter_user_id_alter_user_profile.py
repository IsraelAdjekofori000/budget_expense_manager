# Generated by Django 5.0.7 on 2024-09-21 00:21

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0003_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('824a8b91-46a0-4f91-8b15-3bd5f4718043'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
