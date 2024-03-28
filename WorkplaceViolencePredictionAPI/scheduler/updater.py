from apscheduler.schedulers.background import BackgroundScheduler

from WorkplaceViolencePredictionAPI.scheduler import tasks

# (tasks.FUNCTION, INTERVAL_IN_SECONDS)
jobs = [
    (tasks.hello_world, 5)
]


def start():
    scheduler = BackgroundScheduler()

    for job in jobs:
        scheduler.add_job(job[0], 'interval', seconds=job[1])

    scheduler.start()
