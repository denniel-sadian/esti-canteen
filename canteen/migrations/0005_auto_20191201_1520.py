# Generated by Django 2.2.4 on 2019-12-01 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0004_auto_20191201_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='date',
            field=models.DateField(),
        ),
    ]