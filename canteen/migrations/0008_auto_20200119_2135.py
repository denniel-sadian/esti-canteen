# Generated by Django 2.2.8 on 2020-01-19 13:35

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0007_auto_20200112_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='photo',
            field=django_resized.forms.ResizedImageField(crop=None, force_format='PNG', keep_meta=True, quality=0, size=[500, 500], upload_to=''),
        ),
    ]
