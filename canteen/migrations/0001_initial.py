# Generated by Django 2.2 on 2019-07-31 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('date', models.DateField(auto_now=True)),
                ('description', models.CharField(max_length=101)),
                ('sold_out', models.BooleanField(default=False)),
                ('photo', models.ImageField(upload_to='dishes')),
            ],
            options={
                'verbose_name_plural': 'dishes',
                'unique_together': {('name', 'date')},
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('contact_no', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=100)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('id_no', models.CharField(max_length=100, verbose_name='id no.')),
                ('contact_no', models.CharField(max_length=15)),
                ('count', models.IntegerField(default=1)),
                ('amount', models.FloatField(editable=False)),
                ('served', models.BooleanField(default=False)),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canteen.Dish')),
            ],
        ),
    ]
