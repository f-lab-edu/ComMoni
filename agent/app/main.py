import asyncio

from sig.setting import set_signal
from schedule.scheduler import Scheduler

from app.token_manage.manager import token_manager
from app.configs.log import logger


async def main():
    # signal setting
    set_signal(asyncio.get_running_loop())
    logger.info("[main] Run Commoni Agent...")

    # agent_scheduler = Scheduler()
    # agent_scheduler.add_cron_schedule(
    #     func=send_reailtime_data,
    #     second=f'*/{settings.REALTIME_SEND_INTERVAL}',
    #     args=None)

    try:
        while True:
            await asyncio.sleep(1000)
    except asyncio.CancelledError:
        logger.error("[main] agent main catch Asyncio-CancelledError")

    # agent_scheduler.shutdown()


# agent run
asyncio.run(main())
