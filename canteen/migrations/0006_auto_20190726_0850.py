# Generated by Django 2.2 on 2019-07-26 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0005_auto_20190726_0845'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='datetime',
            new_name='date',
        ),
    ]