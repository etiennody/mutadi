# Generated by Django 3.1.4 on 2020-12-27 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('private_messages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privatemessage',
            name='conversation',
        ),
        migrations.AddField(
            model_name='privatemessage',
            name='subject',
            field=models.CharField(default=True, max_length=150),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='privatemessage',
            name='recipient',
        ),
        migrations.AddField(
            model_name='privatemessage',
            name='recipient',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='auth.user'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Conversation',
        ),
    ]
