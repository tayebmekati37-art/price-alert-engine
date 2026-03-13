from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
import logging

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def start_scheduler(app):
    with app.app_context():
        interval = app.config['CHECK_INTERVAL']
        from .alert_checker import check_alerts
        # Pass app as argument to the job function
        scheduler.add_job(
            func=check_alerts,
            args=[app],
            trigger=IntervalTrigger(seconds=interval),
            id='check_alerts',
            name='Check price alerts',
            replace_existing=True
        )
        scheduler.start()
        logger.info(f"Scheduler started, checking every {interval} seconds")

        atexit.register(lambda: scheduler.shutdown())