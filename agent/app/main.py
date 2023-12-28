import asyncio

from sig.setting import set_signal
from app.auth.login_manager import login_api_server

from app.schedule.scheduler import Scheduler
from app.schedule.monitoring import send_rt_monitoring, send_monitoring

from app.configs.config import settings
from app.configs.log import logger


async def main():
    # signal setting
    set_signal(asyncio.get_running_loop())
    logger.info("[main] Run Commoni Agent...")

    await login_api_server()

    agent_scheduler = Scheduler()
    agent_scheduler.add_cron_schedule(
        func=send_rt_monitoring,
        second=f'*/{settings.REALTIME_INTERVAL}',
        args=None)

    agent_scheduler.add_cron_schedule(
        func=send_monitoring,
        second=f'*/{settings.NORMAL_INTERVAL}',
        args=None)

    try:
        while True:
            await asyncio.sleep(100)
    except asyncio.CancelledError:
        logger.error("[main] agent main catch Asyncio-CancelledError")

    agent_scheduler.shutdown()


# agent run
asyncio.run(main())
