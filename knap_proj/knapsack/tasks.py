import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task
from celery.result import AsyncResult


from ortools.algorithms import pywrapknapsack_solver



@shared_task
def knapsack_solver(capacity, values, weights):
    solver = pywrapknapsack_solver.KnapsackSolver(pywrapknapsack_solver.KnapsackSolver.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,'test')
    import time
    time.sleep(15)

    solver.Init(values, weights, capacity)
    computed_value = solver.Solve()

    packed_items = [x for x in range(0, len(weights[0]))
                    if solver.BestSolutionContains(x)]
    packed_weights = [weights[0][i] for i in packed_items]
    total_weight = sum(packed_weights)

    return packed_items,packed_weights,computed_value,total_weight


#@shared_task
def knapsack_solver_status(task_id):
    res = AsyncResult(task_id)
    return res