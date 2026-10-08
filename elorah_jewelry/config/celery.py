import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
app = Celery("elorah_jewelry")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Periodic tasks
app.conf.beat_schedule = {
    "release-abandoned-stock": {
        "task": "apps.payments.tasks.release_abandoned_payments",
        "schedule": crontab(minute="*/5"),  # Every 5 minutes
    },
    "cleanup-expired-sessions": {
        "task": "apps.core.tasks.cleanup_expired_sessions",
        "schedule": crontab(hour=3, minute=0),  # Daily 3 AM
    },
    "audit-log-retention": {
        "task": "apps.audit.tasks.cleanup_old_audit_logs",
        "schedule": crontab(day_of_month=1, hour=2),  # Monthly
    },
}
