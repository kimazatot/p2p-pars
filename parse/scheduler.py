import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import parse_p2p

scheduler = BackgroundScheduler()

def start():
    scheduler.add_job(
        lambda: asyncio.run(parse_p2p()),
        trigger='cron',
        hour='11,17',
        minute=0,
        id='p2p_parser',
        replace_existing=True
    )
    scheduler.start()
