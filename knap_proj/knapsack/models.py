from django.db import models

# Create your models here.


class TasksStats(models.Model):
    task_id = models.CharField(max_length=100, default=None)
    time_submitted = models.FloatField(null=True, default=None)
    time_started = models.FloatField(null=True, default=None)
    time_completed = models.FloatField(null=True, default=None)


class Problem(models.Model):

    task_id = models.CharField(max_length=100, default=None)
    capacity = models.IntegerField()
    weights = models.TextField()
    values = models.TextField()


class Solution(models.Model):

    task_id = models.CharField(max_length=100, default=None)
    items = models.TextField()
    time = models.FloatField(null=True)
