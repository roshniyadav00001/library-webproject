# Generated by Django 5.0 on 2023-12-27 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_category_alter_mybook_category'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Categorymodel',
        ),
    ]
