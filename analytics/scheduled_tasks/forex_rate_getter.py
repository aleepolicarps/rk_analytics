from analytics import app, db_conn
from analytics.models import ForExRates
from sqlalchemy import update
import json
import requests
from datetime import datetime
import pytz


class ForExRateGetter:

    def update_forex_rates(self):
        app.logger.info('Getting forex rates')
        response = requests.get('https://api.fixer.io/latest?base=EUR')
        data = response.json()
        rates = data['rates']
        now = datetime.now(pytz.timezone('Europe/Copenhagen'))

        for currency, rate in rates.iteritems():
            forex_rate = ForExRates.select(ForExRates.c.currency == currency).execute().first()
            if forex_rate:
                ForExRates.update().where(ForExRates.c.currency == currency).values(rate=rate, updated_at=now).execute()
            else:
                db_conn.execute(ForExRates.insert(), currency=currency, rate=rate)
