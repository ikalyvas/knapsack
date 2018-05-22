import time

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
    #print("task state"+str(res.))
    return JsonResponse({"task": task_id,
                         "status": "submitted",
                         "timestamps":
                             {"submitted": int(time.time()),
                              "started": None, "completed": None}
                         })


def get_task(request, task_id):

    res = tasks.knapsack_solver_status(task_id)
    print("State of task %s:[%s]" %(task_id, res.state))
    return JsonResponse({"task": task_id,
                         "status": "submitted",
                         "state": res.status,
                         "timestamps":
                             {"submitted": 1505225308,
                              "started": 1505225320,
                              "completed": None
                              }
                         })
