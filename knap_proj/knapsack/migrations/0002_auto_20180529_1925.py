# Generated by Django 2.0.5 on 2018-05-29 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knapsack', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celeryresults',
            name='time_completed',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='celeryresults',
            name='time_started',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='celeryresults',
            name='time_submitted',
            field=models.FloatField(null=True),
        ),
    ]
