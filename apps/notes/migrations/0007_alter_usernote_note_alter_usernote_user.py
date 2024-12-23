# Generated by Django 5.1.1 on 2024-10-08 20:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_alter_usernote_note_alter_usernote_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernote',
            name='note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='note_user', to='notes.note'),
        ),
        migrations.AlterField(
            model_name='usernote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_note', to=settings.AUTH_USER_MODEL),
        ),
    ]
