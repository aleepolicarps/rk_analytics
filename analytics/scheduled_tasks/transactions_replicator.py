from analytics import db_conn, config, app
from analytics.models import Transactions
from sqlalchemy import desc, create_engine, func, select, engine
from sqlalchemy.sql import text
from sshtunnel import SSHTunnelForwarder
from datetime import datetime, timedelta
import MySQLdb as db
import json


class TransactionsReplicator:

    def replicate_sd_transactions(self):
        app.logger.info('Starting replication on SD')
        account_name = config['sd_account_name']
        last_id = select([func.max(Transactions.c.original_id)]).where(Transactions.c.account == account_name).execute().first()
        last_id = last_id[0] if last_id[0] else 0

        connection_string = config['sd_connection_string'] + '?charset=utf8'
        source_engine = create_engine(connection_string)
        source_conn = source_engine.connect()
        sql = text('''SELECT * FROM maxpay_charge_new
            WHERE maxpay_charge_new.id > :last_id
            ORDER BY maxpay_charge_new.id ASC
            LIMIT :count''')
        result = source_conn.execute(sql, last_id=int(last_id), count=100).fetchall()

        charges = []
        for charge in result:
            sql = text('''SELECT temp_users.webid as webid, webid.country AS country FROM temp_users
                JOIN webid ON webid.web_id = temp_users.webid
                WHERE temp_users.cust_id = :customer_id''')
            user_info = source_conn.execute(sql, customer_id=charge['merchant_user_id']).first()

            if not user_info:
                sql = text('''SELECT users.webid AS webid, webid.country AS country FROM users
                    JOIN webid ON webid.web_id = users.webid
                    WHERE users.customer_id = :customer_id''')
                user_info = source_conn.execute(sql, customer_id=charge['merchant_user_id']).first()

            if not user_info:
                user_info = dict(webid=None, country=None)

            charge_temp = dict(charge)
            charge_temp['webid'] = user_info['webid']
            charge_temp['webid_country'] = user_info['country']
            charges.append(charge_temp)

        source_conn.close()

        values = []
        for charge in charges:
            app.logger.info('Inserting transaction id = %i, account = %s' % (charge['id'], account_name))
            created_at = charge['date_created'] - timedelta(hours=1)
            response = json.loads(charge['charges_response'])
            mid_name = response['custom_fields']['custom_mid_name']

            values.append(dict(account=account_name, merchant_user_id=charge['merchant_user_id'], transaction_type=charge['transaction_type'],
                               mode=charge['mode'], code=int(charge['code']) if charge['code'] else 0, amount=charge['amount'], currency=charge['currency'],
                               card_holder=charge['card_holder'], brand=charge['brand'], bank=charge['bank'], level=charge['level'],
                               type=charge['type'], bin=charge['bin'], last=charge['last'], exp_month=charge['exp_month'],
                               exp_year=charge['exp_year'], bank_id=charge['bank_id'], bank_authcode=charge['bank_authcode'],
                               bank_time=charge['bank_time'], charge_time=charge['charge_time'], token=charge['token'],
                               reference=charge['reference'], base_reference=charge['base_reference'], transaction_unique_id=charge['transaction_unique_id'],
                               fraudulent=charge['is_fraudalerts'], created_at=created_at, response=charge['charges_response'],
                               webid=charge['webid'], country=charge['webid_country'], original_id=charge['id'], status=charge['status'],
                               mid_name=mid_name))

        if values:
            db_conn.execute(Transactions.insert(), values)

        app.logger.info('Finished replication on SD')

    def replicate_bb_transactions(self):
        app.logger.info('Starting replication on BB')
        account_name = config['bb_account_name']
        last_id = select([func.max(Transactions.c.original_id)]).where(Transactions.c.account == account_name).execute().first()
        app.logger.info(last_id)
        last_id = last_id[0] if last_id[0] else 0
        app.logger.info(last_id)

        connection_string = config['bb_connection_string'] + '?charset=utf8'
        source_engine = create_engine(connection_string)
        source_conn = source_engine.connect()
        sql = text('''SELECT * FROM maxpay_charge_new
            WHERE maxpay_charge_new.id > :last_id
            ORDER BY maxpay_charge_new.id ASC
            LIMIT :count''')
        result = source_conn.execute(sql, last_id=int(last_id), count=100).fetchall()

        charges = []
        for charge in result:
            sql = text('''SELECT temp_users.webid as webid, webid.country AS country FROM temp_users
                JOIN webid ON webid.web_id = temp_users.webid
                WHERE temp_users.cust_id = :customer_id''')
            user_info = source_conn.execute(sql, customer_id=charge['merchant_user_id']).first()

            if not user_info:
                sql = text('''SELECT users.webid AS webid, webid.country AS country FROM users
                    JOIN webid ON webid.web_id = users.webid
                    WHERE users.customer_id = :customer_id''')
                user_info = source_conn.execute(sql, customer_id=charge['merchant_user_id']).first()

            if not user_info:
                user_info = dict(webid=None, country=None)

            charge_temp = dict(charge)
            charge_temp['webid'] = user_info['webid']
            charge_temp['webid_country'] = user_info['country']
            charges.append(charge_temp)

        source_conn.close()

        values = []
        for charge in charges:
            app.logger.info('Inserting transaction id = %i, account = %s' % (charge['id'], account_name))
            created_at = charge['date_created'] - timedelta(hours=1)
            response = json.loads(charge['charges_response'])
            mid_name = response['custom_fields']['custom_mid_name']

            values.append(dict(account=account_name, merchant_user_id=charge['merchant_user_id'], transaction_type=charge['transaction_type'],
                               mode=charge['mode'], code=int(charge['code']) if charge['code'] else 0, amount=charge['amount'], currency=charge['currency'],
                               card_holder=charge['card_holder'], brand=charge['brand'], bank=charge['bank'], level=charge['level'],
                               type=charge['type'], bin=charge['bin'], last=charge['last'], exp_month=charge['exp_month'],
                               exp_year=charge['exp_year'], bank_id=charge['bank_id'], bank_authcode=charge['bank_authcode'],
                               bank_time=charge['bank_time'], charge_time=charge['charge_time'], token=charge['token'],
                               reference=charge['reference'], base_reference=charge['base_reference'], transaction_unique_id=charge['transaction_unique_id'],
                               fraudulent=charge['is_fraudalerts'], created_at=created_at, response=charge['charges_response'],
                               webid=charge['webid'], country=charge['webid_country'], original_id=charge['id'], status=charge['status'],
                               mid_name=mid_name))

        if values:
            db_conn.execute(Transactions.insert(), values)

        app.logger.info('Finished replication on BB')

    def replicate_pb_transactions(self):
        app.logger.info('Starting replication on PB')
        account_name = config['pb_account_name']
        last_id = select([func.max(Transactions.c.original_id)]).where(Transactions.c.account == account_name).execute().first()
        last_id = last_id[0] if last_id[0] else 0

        charges = []
        with SSHTunnelForwarder(
                (config['pb_ssh_host'], int(config['pb_ssh_port'])),
                ssh_username=config['pb_ssh_username'],
                ssh_password=config['pb_ssh_password'],
                remote_bind_address=('127.0.0.1', 3306),
                local_bind_address=('127.0.0.1', 3307)) as server:

            connection_string = config['pb_connection_string'] + '?charset=utf8'
            source_engine = create_engine(connection_string)
            source_conn = source_engine.connect()
            sql = text('''SELECT * FROM maxpay_charge_new
                WHERE maxpay_charge_new.id > :last_id
                ORDER BY maxpay_charge_new.id ASC
                LIMIT :count''')
            result = source_conn.execute(sql, last_id=int(last_id), count=100).fetchall()

            for charge in result:
                sql = text('''SELECT temp_users.webid as webid, webid.country AS country FROM temp_users
                    JOIN webid ON webid.web_id = temp_users.webid
                    WHERE temp_users.cust_id = :customer_id''')
                user_info = source_conn.execute(sql, customer_id=charge['merchant_user_id']).first()

                if not user_info:
                    sql = text('''SELECT users.webid AS webid, webid.country AS country FROM users
                        JOIN webid ON webid.web_id = users.webid
                        WHERE users.customer_id = :customer_id''')
                    user_info = source_conn.execute(sql, customer_id=charge['merchant_user_id']).first()

                if not user_info:
                    user_info = dict(webid=None, country=None)

                charge_temp = dict(charge)
                charge_temp['webid'] = user_info['webid']
                charge_temp['webid_country'] = user_info['country']
                charges.append(charge_temp)

            source_conn.close()

        values = []
        for charge in charges:
            app.logger.info('Inserting transaction id = %i, account = %s' % (charge['id'], account_name))
            created_at = charge['date_created'] - timedelta(hours=1)
            response = json.loads(charge['charges_response'])
            mid_name = response['custom_fields']['custom_mid_name']

            values.append(dict(account=account_name, merchant_user_id=charge['merchant_user_id'], transaction_type=charge['transaction_type'],
                               mode=charge['mode'], code=int(charge['code']) if charge['code'] else 0, amount=charge['amount'], currency=charge['currency'],
                               card_holder=charge['card_holder'], brand=charge['brand'], bank=charge['bank'], level=charge['level'],
                               type=charge['type'], bin=charge['bin'], last=charge['last'], exp_month=charge['exp_month'],
                               exp_year=charge['exp_year'], bank_id=charge['bank_id'], bank_authcode=charge['bank_authcode'],
                               bank_time=charge['bank_time'], charge_time=charge['charge_time'], token=charge['token'],
                               reference=charge['reference'], base_reference=charge['base_reference'], transaction_unique_id=charge['transaction_unique_id'],
                               fraudulent=charge['is_fraudalerts'], created_at=created_at, response=charge['charges_response'],
                               webid=charge['webid'], country=charge['webid_country'], original_id=charge['id'], status=charge['status'],
                               mid_name=mid_name))

        if values:
            db_conn.execute(Transactions.insert(), values)

        app.logger.info('Finished replication on PB')
