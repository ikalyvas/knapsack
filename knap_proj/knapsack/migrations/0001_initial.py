# Generated by Django 2.0.5 on 2018-05-30 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(default=None, max_length=100)),
                ('capacity', models.IntegerField()),
                ('weights', models.TextField()),
                ('values', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(default=None, max_length=100)),
                ('items', models.TextField()),
                ('time', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TasksStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(default=None, max_length=100)),
                ('time_submitted', models.FloatField(null=True)),
                ('time_started', models.FloatField(null=True)),
                ('time_completed', models.FloatField(null=True)),
            ],
        ),
    ]
