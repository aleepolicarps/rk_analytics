from analytics import db_conn, config, app
from analytics.models import Transactions
from sqlalchemy import desc, create_engine, func, select
from sqlalchemy.sql import text
from sshtunnel import SSHTunnelForwarder
import MySQLdb as db

class TransactionsReplicator:

    def replicate_sd_transactions(self):
        app.logger.info('Starting replication on SD')
        account_name = config['sd_account_name']
        last_id = select([func.max(Transactions.c.original_id)]).where(Transactions.c.account == account_name).execute().first()
        last_id = last_id[0] if last_id[0] else 0

        connection_string = config['sd_connection_string']
        source_engine = create_engine(connection_string)
        source_conn = source_engine.connect()
        sql = text('''SELECT maxpay_charge_new.*, webid.web_id AS webid, webid.country AS web_id_country FROM maxpay_charge_new
            LEFT JOIN users ON users.customer_id = maxpay_charge_new.merchant_user_id
            LEFT JOIN webid ON users.webid = webid.web_id
            WHERE maxpay_charge_new.id > :last_id
            ORDER BY maxpay_charge_new.id ASC
            LIMIT :count''')
        result = source_conn.execute(sql, last_id=last_id, count=100).fetchall()
        source_conn.close()

        values = []
        for charge in result:
            app.logger.info('Inserting transaction id = %i, account = %s' % (charge['id'], account_name))
            values.append(dict(account=account_name, merchant_user_id=charge['merchant_user_id'], transaction_type=charge['transaction_type'],
            mode=charge['mode'], code=charge['code'], amount=charge['amount'], currency=charge['currency'],
            card_holder=charge['card_holder'], brand=charge['brand'], bank=charge['bank'], level=charge['level'],
            type=charge['type'], bin=charge['bin'], last=charge['last'], exp_month=charge['exp_month'],
            exp_year=charge['exp_year'], bank_id=charge['bank_id'], bank_authcode=charge['bank_authcode'],
            bank_time=charge['bank_time'], charge_time=charge['charge_time'], token=charge['token'],
            reference=charge['reference'], base_reference=charge['base_reference'], transaction_unique_id=charge['transaction_unique_id'],
            fraudulent=charge['is_fraudalerts'], created_at=charge['date_created'], response=charge['charges_response'],
            webid=charge['webid'], country=charge['web_id_country'], original_id=charge['id'], status=charge['status']))

        db_conn.execute(Transactions.insert(), values)
        app.logger.info('Finished replication on SD')

    def replicate_bb_transactions(self):
        app.logger.info('Starting replication on BB')
        account_name = config['bb_account_name']
        last_id = select([func.max(Transactions.c.original_id)]).where(Transactions.c.account == account_name).execute().first()
        app.logger.info(last_id)
        last_id = last_id[0] if last_id[0] else 0
        app.logger.info(last_id)

        connection_string = config['bb_connection_string']
        source_engine = create_engine(connection_string)
        source_conn = source_engine.connect()
        sql = text('''SELECT maxpay_charge_new.*, webid.web_id AS webid, webid.country AS web_id_country FROM maxpay_charge_new
            LEFT JOIN users ON users.customer_id = maxpay_charge_new.merchant_user_id
            LEFT JOIN webid ON users.webid = webid.web_id
            WHERE maxpay_charge_new.id > :last_id
            ORDER BY maxpay_charge_new.id ASC
            LIMIT :count''')
        result = source_conn.execute(sql, last_id=last_id, count=100).fetchall()
        app.logger.info(len(result))
        source_conn.close()

        values = []
        for charge in result:
            app.logger.info('Inserting transaction id = %i, account = %s' % (charge['id'], account_name))
            values.append(dict(account=account_name, merchant_user_id=charge['merchant_user_id'], transaction_type=charge['transaction_type'],
            mode=charge['mode'], code=charge['code'], amount=charge['amount'], currency=charge['currency'],
            card_holder=charge['card_holder'], brand=charge['brand'], bank=charge['bank'], level=charge['level'],
            type=charge['type'], bin=charge['bin'], last=charge['last'], exp_month=charge['exp_month'],
            exp_year=charge['exp_year'], bank_id=charge['bank_id'], bank_authcode=charge['bank_authcode'],
            bank_time=charge['bank_time'], charge_time=charge['charge_time'], token=charge['token'],
            reference=charge['reference'], base_reference=charge['base_reference'], transaction_unique_id=charge['transaction_unique_id'],
            fraudulent=charge['is_fraudalerts'], created_at=charge['date_created'], response=charge['charges_response'],
            webid=charge['webid'], country=charge['web_id_country'], original_id=charge['id'], status=charge['status']))

        db_conn.execute(Transactions.insert(), values)
        app.logger.info('Finished replication on BB')

    def replicate_fb_transactions(self):
        app.logger.info('Starting replication on FB')
        account_name = config['fb_account_name']
        last_id = select([func.max(Transactions.c.original_id)]).where(Transactions.c.account == account_name).execute().first()
        last_id = last_id[0] if last_id[0] else 0

        result = []
        with SSHTunnelForwarder(
            (config['fb_ssh_host'], config['fb_ssh_port']),
            ssh_username=config['fb_ssh_username'],
            ssh_password=config['fb_ssh_password'],
            remote_bind_address=('127.0.0.1', 3306),
            local_bind_address = ('127.0.0.1', 3307),
            ) as server:

            connection_string = config['fb_connection_string']
            source_engine = create_engine(connection_string)
            source_conn = source_engine.connect()
            sql = text('''SELECT maxpay_charge_new.*, webid.web_id AS webid, webid.country AS web_id_country FROM maxpay_charge_new
                LEFT JOIN users ON users.customer_id = maxpay_charge_new.merchant_user_id
                LEFT JOIN webid ON users.webid = webid.web_id
                WHERE maxpay_charge_new.id > :last_id
                ORDER BY maxpay_charge_new.id ASC
                LIMIT :count''')
            result = source_conn.execute(sql, last_id=last_id, count=100).fetchall()
            source_conn.close()

        values = []
        for charge in result:
            app.logger.info('Inserting transaction id = %i, account = %s' % (charge['id'], account_name))
            values.append(dict(account=account_name, merchant_user_id=charge['merchant_user_id'], transaction_type=charge['transaction_type'],
                mode=charge['mode'], code=charge['code'], amount=charge['amount'], currency=charge['currency'],
                card_holder=charge['card_holder'], brand=charge['brand'], bank=charge['bank'], level=charge['level'],
                type=charge['type'], bin=charge['bin'], last=charge['last'], exp_month=charge['exp_month'],
                exp_year=charge['exp_year'], bank_id=charge['bank_id'], bank_authcode=charge['bank_authcode'],
                bank_time=charge['bank_time'], charge_time=charge['charge_time'], token=charge['token'],
                reference=charge['reference'], base_reference=charge['base_reference'], transaction_unique_id=charge['transaction_unique_id'],
                fraudulent=charge['is_fraudalerts'], created_at=charge['date_created'], response=charge['charges_response'],
                webid=charge['webid'], country=charge['web_id_country'], original_id=charge['id'], status=charge['status']))

        db_conn.execute(Transactions.insert(), values)
        app.logger.info('Finished replication on FB')

    def replicate_pb_transactions(self):
        app.logger.info('Starting replication on PB')
        account_name = config['pb_account_name']
        last_id = select([func.max(Transactions.c.original_id)]).where(Transactions.c.account == account_name).execute().first()
        last_id = last_id[0] if last_id[0] else 0

        result = []
        with SSHTunnelForwarder(
            (config['pb_ssh_host'], config['pb_ssh_port']),
            ssh_username=config['pb_ssh_username'],
            ssh_password=config['pb_ssh_password'],
            remote_bind_address=('127.0.0.1', 3306),
            local_bind_address = ('127.0.0.1', 3307),
            ) as server:

            connection_string = config['pb_connection_string']
            source_engine = create_engine(connection_string)
            source_conn = source_engine.connect()
            sql = text('''SELECT maxpay_charge_new.*, webid.web_id AS webid, webid.country AS web_id_country FROM maxpay_charge_new
                LEFT JOIN users ON users.customer_id = maxpay_charge_new.merchant_user_id
                LEFT JOIN webid ON users.webid = webid.web_id
                WHERE maxpay_charge_new.id > :last_id
                ORDER BY maxpay_charge_new.id ASC
                LIMIT :count''')
            result = source_conn.execute(sql, last_id=last_id, count=100).fetchall()
            source_conn.close()

        values = []
        for charge in result:
            app.logger.info('Inserting transaction id = %i, account = %s' % (charge['id'], account_name))
            values.append(dict(account=account_name, merchant_user_id=charge['merchant_user_id'], transaction_type=charge['transaction_type'],
                mode=charge['mode'], code=charge['code'], amount=charge['amount'], currency=charge['currency'],
                card_holder=charge['card_holder'], brand=charge['brand'], bank=charge['bank'], level=charge['level'],
                type=charge['type'], bin=charge['bin'], last=charge['last'], exp_month=charge['exp_month'],
                exp_year=charge['exp_year'], bank_id=charge['bank_id'], bank_authcode=charge['bank_authcode'],
                bank_time=charge['bank_time'], charge_time=charge['charge_time'], token=charge['token'],
                reference=charge['reference'], base_reference=charge['base_reference'], transaction_unique_id=charge['transaction_unique_id'],
                fraudulent=charge['is_fraudalerts'], created_at=charge['date_created'], response=charge['charges_response'],
                webid=charge['webid'], country=charge['web_id_country'], original_id=charge['id'], status=charge['status']))

        db_conn.execute(Transactions.insert(), values)
        app.logger.info('Finished replication on PB')
