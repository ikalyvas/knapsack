import time
from .models import TasksStats
from django.shortcuts import render, redirect
from django.http import  HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
# Create your views here.

from . import tasks


@csrf_exempt
def create_tasks(request):

    dict_body = eval(request.body)
    capacity = dict_body.get('problem', None).get('capacity', 0)
    values = dict_body.get('problem', None).get('values', 0)
    weights = dict_body.get('problem', None).get('weights', 0)

    res = tasks.knapsack_solver.delay([capacity], values, [weights])

    task_id = res.task_id

    while True:
        try:
            task_ = TasksStats.objects.get(task_id = task_id)
        except TasksStats.DoesNotExist:
            print("Not written into the db yet...retrying")
            continue
        else:
            break

    return JsonResponse({"task": task_id,
                         "status": "submitted",
                         "timestamps":
                             {"submitted": task_.time_submitted,
                              "started": None, "completed": None}
                         })


def get_task(request, task_id):

    res = tasks.knapsack_solver_status(task_id)
    print("State of task %s:[%s]" %(task_id, res.state))
    task_ = TasksStats.objects.get(task_id = task_id)
    time_started = task_.time_started if task_.time_started != None else None
    time_submitted = task_.time_submitted
    time_completed = task_.time_completed if task_.time_completed != None else None

    return JsonResponse({"task": task_id,
                         "status": "submitted",
                         "state": res.status,
                         "timestamps":
                             {"submitted": time_submitted,
                              "started": time_started,
                              "completed": time_completed
                              }
                         })
