# Generated by Django 5.0.2 on 2024-05-18 15:13

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(default=uuid.uuid4, max_length=255, primary_key=True, serialize=False),
        ),
    ]
