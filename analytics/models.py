from analytics import metadata
from sqlalchemy import Table

UserActions = Table('user_actions', metadata, autoload=True)
Transactions = Table('transactions', metadata, autoload=True)
Chargebacks = Table('chargebacks', metadata, autoload=True)
ForExRates = Table('forex_rates', metadata, autoload=True)
FacebookAdReports = Table('facebook_ad_reports', metadata, autoload=True)
LogData = Table('log_data', metadata, autoload=True)
