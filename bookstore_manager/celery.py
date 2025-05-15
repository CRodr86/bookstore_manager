import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore_manager.settings')

# Celery app instance
app = Celery('bookstore_manager')

# Load Celery settings from Django settings with a CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Schedule periodic tasks to check for restock events every minute
app.conf.beat_schedule = {
    'process_restock_events_every_minute': {
        'task' : 'books.tasks.process_restock_events',
        'schedule': 60.0,
    },
}