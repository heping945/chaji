BROKER_URL = 'redis://localhost:6379/7'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/8'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Shanghai'