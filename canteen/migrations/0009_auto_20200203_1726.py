# Generated by Django 2.2.8 on 2020-02-03 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0008_auto_20200119_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='contact_no',
            field=models.CharField(max_length=12),
        ),
    ]
