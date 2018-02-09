from apscheduler.schedulers.background import BackgroundScheduler
from transactions_replicator import TransactionsReplicator
from chargebacks_replicator import ChargebacksReplicator
from pytz import utc
import time
import atexit

def print_date_time():
    print time.strftime("%A, %d. %B %Y %I:%M:%S %p")

scheduler = BackgroundScheduler(timezone=utc)
scheduler.start()

transactions_replicator = TransactionsReplicator()
chargebacks_replicator = ChargebacksReplicator()

scheduler.add_job(chargebacks_replicator.replicate_sd_chargebacks, 'interval', minutes=5)
scheduler.add_job(chargebacks_replicator.replicate_fb_chargebacks, 'interval', minutes=5)
scheduler.add_job(chargebacks_replicator.replicate_bb_chargebacks, 'interval', minutes=5)
scheduler.add_job(chargebacks_replicator.replicate_pb_chargebacks, 'interval', minutes=5)

scheduler.add_job(transactions_replicator.replicate_fb_transactions, 'interval', minutes=5)
scheduler.add_job(transactions_replicator.replicate_pb_transactions, 'interval', minutes=5)
scheduler.add_job(transactions_replicator.replicate_bb_transactions, 'interval', minutes=5)
scheduler.add_job(transactions_replicator.replicate_sd_transactions, 'interval', minutes=5)

scheduler.print_jobs()
atexit.register(lambda: scheduler.shutdown())
