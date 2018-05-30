from .celery import app
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knap.settings')
django.setup()

from knapsack.models import TasksStats, Solution


def my_monitor(app):
    state = app.events.State()

    def announce_submitted_tasks(event):
        state.event(event)
        task = state.tasks.get(event['uuid'])

        print("Task: %s[%s] Submitted:%s" % (task.state, task.uuid, task.timestamp))
        task_ = TasksStats(task_id=task.uuid,
                           time_submitted=task.timestamp,
                           time_started=None,
                           time_completed=None)
        task_.save()
        print("Saving submitted task into db")

    def announce_succeeded_tasks(event):
        state.event(event)
        task = state.tasks.get(event['uuid'])

        print("Task: %s[%s] Succeeded at:%s with return value: %s(%s)" % (task.state, task.uuid, task.timestamp, task.result,type(task.result)))
        task_ = TasksStats.objects.get(task_id=task.uuid)
        task_.time_completed = task.timestamp
        task_.save()
        print("Saving succeeding task into db")

        items = eval(task.result)[0]
        time = task_.time_completed - task_.time_started

        solution_ = Solution(task_id=task.uuid, items=items, time=time)
        solution_.save()



    def announce_started_tasks(event):
        state.event(event)
        task = state.tasks.get(event['uuid'])
        
        print("Task %s[%s] Started:%s" % (task.state,task.uuid,task.timestamp))
        task_ = TasksStats.objects.get(task_id=task.uuid)
        task_.time_started = task.timestamp
        task_.save()
        print("Saving started task into db")
    
    def announce_failed_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

        print('TASK FAILED: %s[%s] %s' % (
            task.name, task.uuid, task.info(),))

    with app.connection() as connection:
        print("Starting monitoring")
        recv = app.events.Receiver(connection, handlers={
                'task-failed': announce_failed_tasks,
                'task-started':announce_started_tasks,
                'task-succeeded':announce_succeeded_tasks,
                'task-received':announce_submitted_tasks,
        })
        print("Capturing...")
        recv.capture(limit=None, timeout=None, wakeup=True)


if __name__ == '__main__':
    my_monitor(app)

else:
    print("Not running as main")
    my_monitor(app)