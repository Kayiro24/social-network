# Generated by Django 5.1.1 on 2024-09-23 18:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('friend', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrecord',
            name='friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_friend_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friendrecord',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='friendrecord',
            unique_together={('user', 'friend')},
        ),
    ]
