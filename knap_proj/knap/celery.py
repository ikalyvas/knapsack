import os
import sys

from celery import Celery
from multiprocessing import Process

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knap.settings')

app = Celery('knapsack')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from celery.events import EventReceiver
from kombu import Connection as BrokerConnection

def my_monitor():
    connection = BrokerConnection('amqp://guest:guest@localhost:5672//')

    def on_event(event):
        print("EVENT HAPPENED: ", event)

    def on_task_failed(event):
        exception = event['exception']
        print("TASK FAILED!", event, " EXCEPTION: ", exception)

    while True:
        try:
            with connection as conn:
                recv = EventReceiver(conn,
                                 handlers={'task-failed' : on_task_failed,
                                           'task-succeeded' : on_event,
                                           'task-sent' : on_event,
                                           'task-received' : on_event,
                                           'task-revoked' : on_event,
                                           'task-started' : on_event,
                                           # OR: '*' : on_event
                                           })
            recv.capture(limit=None, timeout=None)
        except (KeyboardInterrupt, SystemExit):
            print("EXCEPTION KEYBOARD INTERRUPT")
            sys.exit()

#p = Process(target=my_monitor)
##p.daemon = True
#p.start()
