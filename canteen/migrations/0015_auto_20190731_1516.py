# Generated by Django 2.2 on 2019-07-31 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0014_dish_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='contact_no',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='order',
            name='contact_no',
            field=models.CharField(max_length=15),
        ),
    ]