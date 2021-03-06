from celery import shared_task
from celery.result import AsyncResult


from ortools.algorithms import pywrapknapsack_solver


@shared_task(bind=True, track_started=True)
def knapsack_solver(self, capacity, values, weights):
    solver = pywrapknapsack_solver.KnapsackSolver(pywrapknapsack_solver.KnapsackSolver.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER,'test')

    solver.Init(values, weights, capacity)
    computed_value = solver.Solve()
    packed_items = [x for x in range(0, len(weights[0]))
                    if solver.BestSolutionContains(x)]
    packed_weights = [weights[0][i] for i in packed_items]
    total_weight = sum(packed_weights)

    return packed_items, packed_weights, computed_value, total_weight


def knapsack_solver_status(task_id):
    res = AsyncResult(task_id)
    return res