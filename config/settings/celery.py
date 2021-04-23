CELERY_BROKER_URL = 'amqp://guest:guest@localhost'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_BACKEND = 'db+postgresql://postgres:123@localhost/example'
