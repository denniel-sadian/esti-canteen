# Generated by Django 2.2 on 2019-07-31 01:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0012_feedback_contact_no'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dish',
            unique_together={('name', 'date')},
        ),
    ]
