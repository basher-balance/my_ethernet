# Generated by Django 4.0.3 on 2022-05-22 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_new_news'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='New',
            new_name='News',
        ),
    ]
