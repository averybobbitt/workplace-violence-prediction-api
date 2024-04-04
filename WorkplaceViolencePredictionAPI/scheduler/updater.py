from apscheduler.schedulers.background import BackgroundScheduler

from WorkplaceViolencePredictionAPI.scheduler import tasks


def start():
    scheduler = BackgroundScheduler(job_defaults={'max_instances': 10})

    #scheduler.add_job(tasks.get_data, 'interval', seconds=10)
    #scheduler.add_job(tasks.predict, 'interval', seconds=10)
    scheduler.add_job(tasks.check_old_logs, 'interval', seconds=3600)

    scheduler.start()
