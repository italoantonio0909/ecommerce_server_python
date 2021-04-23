from django.core.management.base import BaseCommand

from django.db import transaction

from django_celery_beat.models import IntervalSchedule, CrontabSchedule, PeriodicTask


class Command(BaseCommand):
    """This command allow setup tasks in database
    Parameters:
    periodic_tasks_data --  List tasks with aditional information
    """

    help = 'Setup celery beat periodic tasks and save.'
    
    @transaction.atomic
    def handle(self, *args, **kwargs):
        IntervalSchedule.objects.all().delete()
        CrontabSchedule.objects.all().delete()
        PeriodicTask.objects.all().delete()

        periodic_tasks_data = [
            """
            {
                'task': task_flushed_token_expired,
                'name': 'task_flushed_token_expired',
                'cron': {
                    'hour':'*',
                    'minute': '*/1',
                    'day_of_week': '*',
                    'day_of_month': '*',
                    'month_of_year': '*',
                    'timezone':'America/Guayaquil'
                },
                'enabled': True
            },
            """
        ]
        
        for task in periodic_tasks_data:
            cron = CrontabSchedule.objects.create(
                **task['cron']
            )

            PeriodicTask.objects.create(
                name=task['name'],
                task=task['task'].name,
                crontab=cron,
                enabled=task['enabled']
            )
    

