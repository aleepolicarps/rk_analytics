from apscheduler.schedulers.background import BackgroundScheduler
from transactions_replicator import TransactionsReplicator
from pytz import utc
import time
import atexit

def print_date_time():
    print time.strftime("%A, %d. %B %Y %I:%M:%S %p")

scheduler = BackgroundScheduler(timezone=utc)
scheduler.start()

transactions_replicator = TransactionsReplicator()

scheduler.add_job(transactions_replicator.replicate_fb_transactions, 'interval', minutes=5)
scheduler.add_job(transactions_replicator.replicate_pb_transactions, 'interval', minutes=5)
scheduler.add_job(transactions_replicator.replicate_bb_transactions, 'interval', minutes=5)
scheduler.add_job(transactions_replicator.replicate_sd_transactions, 'interval', minutes=5)

scheduler.print_jobs()
atexit.register(lambda: scheduler.shutdown())
