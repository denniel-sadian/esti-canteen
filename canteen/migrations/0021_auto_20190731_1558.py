# Generated by Django 2.2 on 2019-07-31 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0020_auto_20190731_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='count',
            field=models.FloatField(default=1),
        ),
    ]