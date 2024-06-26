# Generated by Django 5.0.4 on 2024-04-14 20:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('estimated_price', models.IntegerField()),
                ('elapsed_time_seconds', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='Object1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Object2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Intermediate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field1', models.DurationField(null=True)),
                ('field2', models.BooleanField(null=True)),
                ('field3', models.DurationField(null=True)),
                ('field4', models.SmallIntegerField(null=True)),
                ('object1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intermediate.object1')),
                ('object2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intermediate.object2')),
            ],
        ),
    ]
