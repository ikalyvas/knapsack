from django.db import models

# Create your models here.


class TasksStats(models.Model):
    task_id = models.CharField(max_length=100, unique=True)
    time_submitted = models.FloatField(null=True)
    time_started = models.FloatField(null=True)
    time_completed = models.FloatField(null=True)


class Solutions(models.Model):
    task = models.ForeignKey(TasksStats, to_field='task_id', on_delete=models.CASCADE)
    capacity = models.IntegerField()
    weights = models.TextField()
    values = models.TextField()

