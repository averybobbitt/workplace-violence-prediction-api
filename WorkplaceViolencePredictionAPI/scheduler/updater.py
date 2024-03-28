from apscheduler.schedulers.background import BackgroundScheduler

from WorkplaceViolencePredictionAPI.scheduler import tasks


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(tasks.hello_world, 'interval', seconds=10)
    scheduler.start()
