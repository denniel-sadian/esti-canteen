# Generated by Django 2.2 on 2019-11-11 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0002_auto_20190810_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
