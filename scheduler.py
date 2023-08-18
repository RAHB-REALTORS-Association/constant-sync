from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
from synchronizer import synchronize_contacts

scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

def start_scheduled_synchronization(interval_hours=2):
    scheduler.add_job(
        func=synchronize_contacts,
        trigger=IntervalTrigger(hours=interval_hours),
        id='scheduled_synchronization_job',
        name='Synchronize JSON contacts with Constant Contact',
        replace_existing=True
    )
