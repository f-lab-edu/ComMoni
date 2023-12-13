import asyncio

from sig.setting import set_signal
from schedule.scheduler import Scheduler
from app.schedule.realtime_sender import send_reailtime_data
from app.configs.config import settings


async def main():
    # signal setting
    set_signal(asyncio.get_running_loop())

    agent_scheduler = Scheduler()

    agent_scheduler.add_cron_schedule(
        func=send_reailtime_data,
        second=f'*/{settings.REALTIME_SEND_INTERVAL}',
        args=None)

    try:
        while True:
            await asyncio.sleep(1000)
    except asyncio.CancelledError:
        print("main catch Asyncio-CancelledError")

    agent_scheduler.shutdown()


# agent run
asyncio.run(main())
