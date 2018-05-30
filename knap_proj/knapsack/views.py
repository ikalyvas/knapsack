import time
from .models import TasksStats, Problem, Solution
from django.shortcuts import get_object_or_404, render, redirect
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

    problem = Problem(task_id=task_id, capacity=capacity, values=values, weights=weights)
    problem.save()

    while True:
        try:
            task_ = TasksStats.objects.get(task_id = task_id)
        except TasksStats.DoesNotExist:
            #print("Not written into the db yet...retrying")
            continue
        else:
            break

    return JsonResponse({"task": task_id,
                         "status": "submitted",
                         "timestamps":
                             {"submitted": task_.time_submitted,
                              "started": None,
                              "completed": None
                              }
                         })


def get_task(request, task_id):

    async_res = tasks.knapsack_solver_status(task_id)
    print("Status of task %s:[%s] -- Solution:%s" %(task_id, async_res.status, async_res.result))
    task_ = TasksStats.objects.get(task_id=task_id)
    time_started = task_.time_started if task_.time_started is not None else None
    time_submitted = task_.time_submitted
    time_completed = task_.time_completed if task_.time_completed is not None else None
    if async_res.status == 'STARTED':
        status = 'started'
    elif async_res.status == 'SUCCESS':
        status = 'completed'
    else:
        status = None

    return JsonResponse({"task": task_id,
                         "status": status,
                         "timestamps":
                             {"submitted": time_submitted,
                              "started": time_started,
                              "completed": time_completed
                              }
                         })


def get_solution(request, task_id):

    solution = get_object_or_404(Solution, task_id=task_id)
    problem = Problem.objects.get(task_id=task_id)

    return JsonResponse({"task": task_id,
                         "problem": {"capacity": problem.capacity,
                                    "weights": problem.weights,
                                    "values": problem.values
                                     },
                         "solution": {"items": solution.items,
                                      "time": solution.time
                                      }
                         }
                        )
