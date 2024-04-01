import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler

from WorkplaceViolencePredictionAPI.scheduler import tasks


def start():
    scheduler = apscheduler.schedulers.background.BackgroundScheduler(job_defaults={'max_instances': 10})

    scheduler.add_job(tasks.get_data, 'interval', seconds= 10)
    scheduler.add_job(tasks.predict, 'interval', seconds = 10)

    scheduler.start()
