# Generated by Django 2.2 on 2019-07-28 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0008_order_served'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='contact_no',
            field=models.IntegerField(default='09453045616'),
            preserve_default=False,
        ),
    ]
