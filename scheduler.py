from apscheduler.schedulers.blocking import BlockingScheduler
from cli import run

sched = BlockingScheduler()

sched.add_job(
    run,
    trigger="cron",
    hour=9,
    minute=30,
    args=["http://localhost:8000"]
)

try:
    print("Scheduler started. Press CTRL+C to stop.")
    sched.start()
except (KeyboardInterrupt, SystemExit):
    print("Scheduler stopped by user.")
    sched.shutdown()
