# Generated by Django 5.0.7 on 2024-08-26 19:37

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('9f425894-b1bf-4a66-8ea3-bce19ddd830e'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
