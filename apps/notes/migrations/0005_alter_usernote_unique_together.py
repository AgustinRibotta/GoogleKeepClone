# Generated by Django 5.1.1 on 2024-09-28 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_alter_usernote_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usernote',
            unique_together=set(),
        ),
    ]
