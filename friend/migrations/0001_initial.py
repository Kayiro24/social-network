# Generated by Django 5.1.1 on 2024-09-23 18:33

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRecord',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='When this instance was created.')),
                ('modified', models.DateTimeField(auto_now=True, help_text='When this instance was modified.')),
                ('status', models.CharField(choices=[('requested', 'Requested'), ('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('removed', 'Removed'), ('blocked', 'Blocked'), ('un_block', 'Un Block')], db_index=True, default='pending', max_length=20)),
            ],
        ),
    ]
