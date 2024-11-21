# Generated by Django 5.1.3 on 2024-11-17 17:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0007_alter_usernote_note_alter_usernote_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='listitems',
            options={'verbose_name': 'List Item', 'verbose_name_plural': 'List Items'},
        ),
        migrations.RemoveField(
            model_name='attachment',
            name='content',
        ),
        migrations.AddField(
            model_name='attachment',
            name='file_path',
            field=models.FileField(null=True, upload_to='attachments/', verbose_name='File Path'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='notes.note'),
        ),
    ]