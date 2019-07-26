# Generated by Django 2.2 on 2019-07-25 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0003_auto_20190725_1106'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dish',
            options={'verbose_name_plural': 'dishes'},
        ),
        migrations.AddField(
            model_name='dish',
            name='description',
            field=models.TextField(default="It's so yummy, that you might forget your name."),
        ),
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.FloatField(editable=False),
        ),
    ]