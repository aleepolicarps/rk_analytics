from analytics import metadata
from sqlalchemy import Table

UserActions = Table('user_actions', metadata, autoload=True)
Transactions = Table('transactions', metadata, autoload=True)
Chargebacks = Table('chargebacks', metadata, autoload=True)
ForExRates = Table('forex_rates', metadata, autoload=True)
