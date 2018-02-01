from analytics import metadata
from sqlalchemy import Table

UserActions = Table('user_actions', metadata, autoload=True)
Transactions = Table('transactions', metadata, autoload=True)
