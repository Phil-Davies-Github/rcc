# Generated by Django 5.0.4 on 2024-05-24 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('yachts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='RecurringEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('order', models.FloatField(default=999)),
                ('duration', models.PositiveSmallIntegerField()),
                ('type', models.CharField(choices=[('Open', 'Open'), ('Club', 'Club')], default='Open', max_length=5)),
                ('location', models.CharField(choices=[('River', 'River'), ('Broad', 'Broad')], default='River', max_length=5)),
                ('code', models.CharField(max_length=20)),
                ('no_races', models.PositiveSmallIntegerField()),
                ('no_discards', models.PositiveSmallIntegerField()),
                ('is_sabrina', models.BooleanField()),
                ('sabrina_order', models.FloatField(blank=True, null=True)),
                ('is_snowbird', models.BooleanField()),
                ('snowbird_order', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('yacht', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='yachts.yacht')),
            ],
            options={
                'verbose_name_plural': 'Event entries',
            },
        ),
        migrations.CreateModel(
            name='EventRace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handicap_applied', models.IntegerField(null=True)),
                ('elapsed_time', models.CharField(max_length=20)),
                ('elapsed_time_seconds', models.IntegerField(blank=True, null=True)),
                ('elapsed_time_minutes', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('corrected_time_seconds', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('corrected_time_minutes', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ('event_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.evententry')),
            ],
        ),
        migrations.CreateModel(
            name='EventOverallRaceResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.eventrace')),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('splits', models.SmallIntegerField()),
                ('order', models.SmallIntegerField()),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
        ),
        migrations.CreateModel(
            name='EventResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.SmallIntegerField(blank=True, null=True)),
                ('points', models.SmallIntegerField(blank=True, null=True)),
                ('margin', models.FloatField()),
                ('handicap_change_to_win', models.FloatField()),
                ('penalty', models.BooleanField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('event_race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.eventrace')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.race')),
            ],
        ),
        migrations.AddField(
            model_name='eventrace',
            name='race',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.race'),
        ),
        migrations.AddField(
            model_name='event',
            name='recurring_event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.recurringevent'),
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('year', models.PositiveSmallIntegerField(primary_key=True, serialize=False, unique=True)),
                ('recurring_events', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='events.recurringevent')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.year'),
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together={('recurring_event', 'year')},
        ),
    ]
