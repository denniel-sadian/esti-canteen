# Generated by Django 2.2 on 2019-07-31 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0019_auto_20190731_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='count',
            field=models.BigIntegerField(),
        ),
    ]
