from apscheduler.schedulers.background import BackgroundScheduler

from WorkplaceViolencePredictionAPI.scheduler import tasks


def start():
    scheduler = BackgroundScheduler()

    scheduler.add_job(tasks.get_data, 'interval', seconds=10)
    scheduler.add_job(tasks.predict, 'interval', seconds = 5)

    scheduler.start()
