# Generated by Django 2.2 on 2019-07-29 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0011_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='contact_no',
            field=models.IntegerField(default='09092304441', verbose_name='contact no.'),
            preserve_default=False,
        ),
    ]