# Generated by Django 2.2 on 2019-07-31 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0016_auto_20190731_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='count',
            field=models.IntegerField(default=1),
        ),
    ]
