from apscheduler.schedulers.background import BackgroundScheduler
from transactions_replicator import TransactionsReplicator
from chargebacks_replicator import ChargebacksReplicator
from forex_rate_getter import ForExRateGetter
from facebook_report_getter import FacebookReportGetter
from pytz import utc
import atexit

scheduler = BackgroundScheduler(timezone=utc)
scheduler.start()

transactions_replicator = TransactionsReplicator()
chargebacks_replicator = ChargebacksReplicator()
facebook_report_getter = FacebookReportGetter()
forex_rate_getter = ForExRateGetter()


def __replicate_pb_tables():
    transactions_replicator.replicate_pb_transactions()
    chargebacks_replicator.replicate_pb_chargebacks()


def __replicate_bb_tables():
    transactions_replicator.replicate_bb_transactions()
    chargebacks_replicator.replicate_bb_chargebacks()


def __replicate_sd_tables():
    transactions_replicator.replicate_sd_transactions()
    chargebacks_replicator.replicate_sd_chargebacks()


scheduler.add_job(__replicate_pb_tables, 'interval', minutes=10)
scheduler.add_job(__replicate_bb_tables, 'interval', minutes=10)
scheduler.add_job(__replicate_sd_tables, 'interval', minutes=10)
scheduler.add_job(forex_rate_getter.update_forex_rates, 'interval', hours=12)
scheduler.add_job(facebook_report_getter.get_bb_reports, 'cron', minute=0)
scheduler.print_jobs()
atexit.register(lambda: scheduler.shutdown())
